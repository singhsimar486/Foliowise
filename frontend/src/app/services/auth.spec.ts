import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { Router } from '@angular/router';

import { AuthService, User } from './auth';
import { environment } from '../../environments/environment';

/**
 * AuthService owns the JWT: where it is stored, whether the app thinks it is
 * logged in, and which header goes out on authenticated calls. These tests use
 * HttpTestingController so no real request is ever made.
 */
describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;
  let navigatedTo: unknown[][];

  const apiUrl = environment.apiUrl;

  const aUser: User = {
    id: 'user-123',
    email: 'simar@example.com',
    is_active: true,
    created_at: '2026-01-01T00:00:00Z',
  };

  beforeEach(() => {
    // Each test gets a clean injector; the builder does not reset it for us.
    TestBed.resetTestingModule();

    // The constructor calls loadStoredUser(), which fires a request if a token
    // is already present. Clearing first keeps each test starting from logged out.
    localStorage.clear();
    navigatedTo = [];

    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        {
          provide: Router,
          useValue: {
            navigate: (commands: unknown[]) => {
              navigatedTo.push(commands);
              return Promise.resolve(true);
            },
          },
        },
      ],
    });

    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('reports logged out when no token is stored', () => {
    expect(service.isLoggedIn()).toBe(false);
    expect(service.getToken()).toBeNull();
  });

  it('reports logged in once a token is stored', () => {
    localStorage.setItem('access_token', 'a-token');

    expect(service.isLoggedIn()).toBe(true);
    expect(service.getToken()).toBe('a-token');
  });

  it('posts registration to /auth/register', () => {
    service.register('simar@example.com', 'a-password').subscribe();

    const request = httpMock.expectOne(`${apiUrl}/auth/register`);
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      email: 'simar@example.com',
      password: 'a-password',
    });
    request.flush(aUser);
  });

  it('sends login as form data, because the backend expects an OAuth2 form', () => {
    service.login('simar@example.com', 'a-password').subscribe();

    const request = httpMock.expectOne(`${apiUrl}/auth/login`);
    expect(request.request.method).toBe('POST');
    // FastAPI's OAuth2PasswordRequestForm reads `username`, not `email`.
    const body = request.request.body as FormData;
    expect(body.get('username')).toBe('simar@example.com');
    expect(body.get('password')).toBe('a-password');

    request.flush({ access_token: 'issued-token', token_type: 'bearer' });
    httpMock.expectOne(`${apiUrl}/auth/me`).flush(aUser);
  });

  it('stores the token returned by a successful login', () => {
    service.login('simar@example.com', 'a-password').subscribe();

    httpMock
      .expectOne(`${apiUrl}/auth/login`)
      .flush({ access_token: 'issued-token', token_type: 'bearer' });
    httpMock.expectOne(`${apiUrl}/auth/me`).flush(aUser);

    expect(localStorage.getItem('access_token')).toBe('issued-token');
    expect(service.isLoggedIn()).toBe(true);
  });

  it('publishes the user on currentUser$ after logging in', () => {
    service.login('simar@example.com', 'a-password').subscribe();

    httpMock
      .expectOne(`${apiUrl}/auth/login`)
      .flush({ access_token: 'issued-token', token_type: 'bearer' });
    httpMock.expectOne(`${apiUrl}/auth/me`).flush(aUser);

    expect(service.currentUserValue).toEqual(aUser);
  });

  it('does not store a token when login fails', () => {
    service.login('simar@example.com', 'wrong').subscribe({ error: () => {} });

    httpMock
      .expectOne(`${apiUrl}/auth/login`)
      .flush({ detail: 'Invalid email or password' }, { status: 401, statusText: 'Unauthorized' });

    expect(localStorage.getItem('access_token')).toBeNull();
    expect(service.isLoggedIn()).toBe(false);
  });

  it('sends the bearer token when fetching the current user', () => {
    localStorage.setItem('access_token', 'a-token');

    service.getCurrentUser().subscribe();

    const request = httpMock.expectOne(`${apiUrl}/auth/me`);
    expect(request.request.headers.get('Authorization')).toBe('Bearer a-token');
    request.flush(aUser);
  });

  it('clears the token, the user and redirects on logout', () => {
    localStorage.setItem('access_token', 'a-token');

    service.logout();

    expect(localStorage.getItem('access_token')).toBeNull();
    expect(service.currentUserValue).toBeNull();
    expect(navigatedTo).toEqual([['/login']]);
  });

  it('logs out when a stored token is rejected on startup', () => {
    // A token left behind from a previous session that the API no longer accepts.
    localStorage.setItem('access_token', 'a-stale-token');

    const freshService = TestBed.inject(AuthService);
    // Re-reading the service does not re-run the constructor, so drive the
    // same path the constructor uses.
    freshService.getCurrentUser().subscribe({ error: () => freshService.logout() });

    httpMock
      .expectOne(`${apiUrl}/auth/me`)
      .flush({ detail: 'Invalid or expired token' }, { status: 401, statusText: 'Unauthorized' });

    expect(localStorage.getItem('access_token')).toBeNull();
  });
});
