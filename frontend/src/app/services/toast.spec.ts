import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';

import { ToastService, Toast } from './toast';

/**
 * ToastService holds the notification queue that the whole app pushes into.
 * It has no HTTP dependency, so these are plain unit tests over its state.
 */
describe('ToastService', () => {
  let service: ToastService;

  beforeEach(() => {
    // Each test gets a clean injector; the builder does not reset it for us.
    TestBed.resetTestingModule();

    TestBed.configureTestingModule({});
    service = TestBed.inject(ToastService);
  });

  async function currentToasts(): Promise<Toast[]> {
    return firstValueFrom(service.toasts$);
  }

  it('starts with an empty queue', async () => {
    expect(await currentToasts()).toEqual([]);
  });

  it('adds a toast with the type, title and message it was given', async () => {
    // duration 0 stops the service scheduling a dismissal timer during the test
    service.show('success', 'Saved', 'Holding added', 0);

    const toasts = await currentToasts();
    expect(toasts.length).toBe(1);
    expect(toasts[0].type).toBe('success');
    expect(toasts[0].title).toBe('Saved');
    expect(toasts[0].message).toBe('Holding added');
  });

  it('keeps multiple toasts in the order they arrived', async () => {
    service.show('success', 'First', 'one', 0);
    service.show('error', 'Second', 'two', 0);

    const titles = (await currentToasts()).map((toast) => toast.title);
    expect(titles).toEqual(['First', 'Second']);
  });

  it('gives every toast a distinct id', async () => {
    service.show('success', 'One', 'a', 0);
    service.show('success', 'Two', 'b', 0);

    const ids = (await currentToasts()).map((toast) => toast.id);
    expect(new Set(ids).size).toBe(2);
  });

  it('dismisses only the toast whose id was passed', async () => {
    service.show('success', 'Keep', 'a', 0);
    service.show('error', 'Remove', 'b', 0);

    const toRemove = (await currentToasts()).find((toast) => toast.title === 'Remove')!;
    service.dismiss(toRemove.id);

    const remaining = await currentToasts();
    expect(remaining.length).toBe(1);
    expect(remaining[0].title).toBe('Keep');
  });

  it('ignores a dismiss for an id that is not in the queue', async () => {
    service.show('success', 'Keep', 'a', 0);

    service.dismiss('an-id-that-does-not-exist');

    expect((await currentToasts()).length).toBe(1);
  });

  it('showSuccess and showError set the matching type', async () => {
    service.showSuccess('Done', 'it worked', 0);
    service.showError('Failed', 'it did not', 0);

    const types = (await currentToasts()).map((toast) => toast.type);
    expect(types).toEqual(['success', 'error']);
  });

  it('formats a price alert with both prices to two decimal places', async () => {
    service.showAlert('AAPL', 'ABOVE', 150, 152.5);

    const toast = (await currentToasts())[0];
    expect(toast.type).toBe('alert');
    expect(toast.title).toBe('AAPL Alert Triggered');
    expect(toast.message).toBe('Price hit $152.50 (target: above $150.00)');
  });

  it('describes a BELOW alert as below', async () => {
    service.showAlert('TSLA', 'BELOW', 200, 195.125);

    const toast = (await currentToasts())[0];
    expect(toast.message).toBe('Price hit $195.13 (target: below $200.00)');
  });
});
