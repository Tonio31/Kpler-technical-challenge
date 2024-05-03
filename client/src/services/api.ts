import type { Position } from '@/models/vessel';

export const BASE_URL: string = 'http://127.0.0.1:5000' as const;

export const wait = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

export const api = async <T>(
  url: string,
  params: RequestInit = {},
  includeContentTypeJson: boolean = true
): Promise<T> => {
  if (includeContentTypeJson) {
    params.headers = Object.assign(
      {
        'Content-Type': 'application/json'
      },
      params.headers
    );
  }

  console.log('TONIO params api params=', params);

  const fullUrl: string = url.startsWith('http') ? url : BASE_URL + url;
  const response: Response = await fetch(fullUrl, params);
  const json: any = (await response.json()) || {};
  console.log('TONIO  api response=', response);
  if (!response.ok) {
    const errorMessage = json.details || response.status;
    console.error(response, `  details=${errorMessage}`);
    return Promise.reject(errorMessage);
  }
  return json as T;
};

export const savePosition = async (position: Position): Promise<Position> => {
  const response: Position = await api<Position>('/vessels/position', {
    method: 'POST',
    body: JSON.stringify(position)
  });
  console.log('\x1b[44m TONIO  addPosition response=', response, '\x1b');
  return response;
};

export const savePositionsInBulk = async (positions: Position[]): Promise<Position[]> => {
  const response: Position[] = await api<Position[]>('/vessels/positions', {
    method: 'POST',
    body: JSON.stringify(positions)
  });
  console.log('\x1b[44m TONIO  addPositions response=', response, '\x1b');
  return response;
};

export const retrieveAllPositions = async (): Promise<Position[]> => {
  const response: Position[] = await api<Position[]>('/vessels/positions', {
    method: 'GET'
  });
  console.log('\x1b[44m TONIO  saveAllPositions response=', response, '\x1b');
  return response;
};

export const deleteAllPositions = async (): Promise<void> => {
  const response: void = await api<void>('/vessels/positions', {
    method: 'DELETE'
  });
  console.log('\x1b[44m TONIO  deleteAllPositions response=', response, '\x1b');
  return response;
};
