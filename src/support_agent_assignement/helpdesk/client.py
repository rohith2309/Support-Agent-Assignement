from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)
from support_agent_assignement.config import settings
import httpx
from .schema import TicketsResponse,Ticket
import time
from support_agent_assignement.utils.sanitizer import sanitize_text

class TransientHelpdeskError(Exception):
    """Raised for retryable 503 or 429 API responses."""
    def __init__(self, status_code: int, message: str, retry_after: float | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.retry_after = retry_after


def _is_retryable_error(exc: BaseException) -> bool:
    return isinstance(exc, (TransientHelpdeskError, httpx.RequestError))


def _wait_with_retry_after(retry_state) -> float:
    exc = retry_state.outcome.exception()
    if isinstance(exc, TransientHelpdeskError) and exc.retry_after is not None:
        return max(exc.retry_after, 0.2)
    # Fallback exponential backoff: 1s, 2s, 4s... up to 15s
    return wait_exponential(multiplier=1, min=1, max=15)(retry_state)

class HelpdeskClient:

    def __init__(self):

        self.client = httpx.AsyncClient(
            verify=False,
            base_url=settings.helpdesk_base_url,
            timeout=30.0,
            headers={
                "X-Candidate-Email":settings.candidate_email,
                "Authorization": f"Bearer {settings.api_key}"
            }
        )
        self._last_request_ts = 0.0
        self._min_interval_sec = 0.25
        
    async def _throttle(self):
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self._min_interval_sec:
            await asyncio.sleep(self._min_interval_sec - elapsed)
        self._last_request_ts = time.monotonic()        

    async def close(self):
        await self.client.aclose()    

    @retry(
    retry=retry_if_exception(httpx.HTTPError),
    stop=stop_after_attempt(5),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=30
    ))
    async def fetch_open_tickets(self,cursor :str|None, limit:int =10 ) -> TicketsResponse:

        reponse = await self.client.get("tickets", params={
            "cursor":cursor,
            "status":"open",
            "limit":limit
        })

        reponse.raise_for_status()

        return TicketsResponse.model_validate(reponse.json())
    
    
    @retry(
        retry=retry_if_exception(_is_retryable_error),
        stop=stop_after_attempt(5),
        wait=_wait_with_retry_after,
        reraise=True,
    )
    async def submit_decision(self, ticket_id: str, action: str, payload: dict) -> dict:
        if action not in {"reply", "handoff", "close"}:
            raise ValueError(f"Invalid action: {action}")

        # Strip None values (e.g., confidence=None) and sanitize all string fields
        clean_payload = {}
        for k, v in payload.items():
            if v is None:
                continue
            clean_payload[k] = sanitize_text(v) if isinstance(v, str) else v

        await self._throttle()
        response = await self.client.post(f"tickets/{ticket_id}/{action}", json=clean_payload)

        # 409 Conflict: ticket already handled — DO NOT retry!
        if response.status_code == 409:
            return {"status": "already_handled", "http_status": 409}

        # 429 Rate Limited: wait Retry-After and retry
        if response.status_code == 429:
            retry_after = float(response.headers.get("Retry-After", "1.0"))
            raise TransientHelpdeskError(
                429, f"Rate limited on POST tickets/{ticket_id}/{action}", retry_after=retry_after
            )

        # 503 Service Unavailable: transient failure (nothing saved), retry with backoff
        if response.status_code == 503:
            raise TransientHelpdeskError(
                503, f"Service unavailable on POST tickets/{ticket_id}/{action}"
            )

        # 400 / 401 / 404 / 422: raise immediately with API validation details
        if response.status_code >= 400:
            raise RuntimeError(
                f"Helpdesk API error {response.status_code} on tickets/{ticket_id}/{action}: {response.text}"
            )

        return {"status": "submitted", "http_status": response.status_code}





