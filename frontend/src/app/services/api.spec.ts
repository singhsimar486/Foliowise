import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { Router } from '@angular/router';

import { ApiService, Holding } from './api';
import { environment } from '../../environments/environment';

/**
 * ApiService is the single place the app talks to the backend. What matters in
 * these tests is that every authenticated call carries the bearer token and
 * hits the URL the FastAPI router actually exposes, including the trailing
 * slash on /holdings/ which FastAPI would otherwise redirect.
 */
describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;

  const apiUrl = environment.apiUrl;

  const aHolding: Holding = {
    id: 'holding-1',
    user_id: 'user-123',
    ticker: 'AAPL',
    quantity: 10,
    avg_cost_basis: 150,
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-01T00:00:00Z',
  };

  beforeEach(() => {
    // Each test gets a clean injector; the builder does not reset it for us.
    TestBed.resetTestingModule();

    // Cleared before injecting, not after: ApiService depends on AuthService,
    // whose constructor fires a GET /auth/me if a token is already in storage.
    // Starting logged out keeps that startup request out of every test.
    localStorage.clear();

    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: Router, useValue: { navigate: () => Promise.resolve(true) } },
      ],
    });

    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);

    // The token is read at request time, so setting it now is enough.
    localStorage.setItem('access_token', 'a-token');
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('gets holdings from /holdings/ with the bearer token', () => {
    let received: Holding[] | undefined;
    service.getHoldings().subscribe((holdings) => (received = holdings));

    const request = httpMock.expectOne(`${apiUrl}/holdings/`);
    expect(request.request.method).toBe('GET');
    expect(request.request.headers.get('Authorization')).toBe('Bearer a-token');
    request.flush([aHolding]);

    expect(received).toEqual([aHolding]);
  });

  it('returns an empty list unchanged', () => {
    let received: Holding[] | undefined;
    service.getHoldings().subscribe((holdings) => (received = holdings));

    httpMock.expectOne(`${apiUrl}/holdings/`).flush([]);

    expect(received).toEqual([]);
  });

  it('posts a new holding with the payload the backend schema expects', () => {
    service
      .createHolding({ ticker: 'AAPL', quantity: 10, avg_cost_basis: 150 })
      .subscribe();

    const request = httpMock.expectOne(`${apiUrl}/holdings/`);
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      ticker: 'AAPL',
      quantity: 10,
      avg_cost_basis: 150,
    });
    expect(request.request.headers.get('Authorization')).toBe('Bearer a-token');
    request.flush(aHolding);
  });

  it('puts an update to the holding id in the path', () => {
    service.updateHolding('holding-1', { quantity: 20 }).subscribe();

    const request = httpMock.expectOne(`${apiUrl}/holdings/holding-1`);
    expect(request.request.method).toBe('PUT');
    expect(request.request.body).toEqual({ quantity: 20 });
    request.flush({ ...aHolding, quantity: 20 });
  });

  it('deletes by id', () => {
    service.deleteHolding('holding-1').subscribe();

    const request = httpMock.expectOne(`${apiUrl}/holdings/holding-1`);
    expect(request.request.method).toBe('DELETE');
    expect(request.request.headers.get('Authorization')).toBe('Bearer a-token');
    request.flush(null);
  });

  it('surfaces a backend error to the caller rather than swallowing it', () => {
    let status: number | undefined;
    service.getHoldings().subscribe({ error: (error) => (status = error.status) });

    httpMock
      .expectOne(`${apiUrl}/holdings/`)
      .flush({ detail: 'Invalid or expired token' }, { status: 401, statusText: 'Unauthorized' });

    expect(status).toBe(401);
  });

  it('still sends an Authorization header when no token is stored', () => {
    // Documents current behaviour: the header is built unconditionally, so a
    // logged out call sends "Bearer null" and the backend answers 401. Worth
    // knowing, because it means the 401 comes from the server, not the client.
    localStorage.removeItem('access_token');

    service.getHoldings().subscribe({ error: () => {} });

    const request = httpMock.expectOne(`${apiUrl}/holdings/`);
    expect(request.request.headers.get('Authorization')).toBe('Bearer null');
    request.flush({ detail: 'Not authenticated' }, { status: 401, statusText: 'Unauthorized' });
  });
});
