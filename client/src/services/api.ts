import type { Position } from '@/models/vessel';

export const BASE_URL: string = 'http://127.0.0.1:5000' as const;

export const api = async <T>(url: string, params: RequestInit = {}): Promise<T> => {
  // params = Object.assign(
  //   {
  //     mode: 'cors',
  //     cache: 'no-cache'
  //   },
  //   params
  // );

  params.headers = Object.assign(
    {
      'Content-Type': 'application/json'
    },
    params.headers
  );

  console.log('TONIO params api params=', params);

  const response: Response = await fetch(BASE_URL + url, params);
  const json: any = (await response.json()) || {};
  if (!response.ok) {
    let errorMessage = json.error || response.status;
    throw new Error(errorMessage);
  }
  return json as T;
};

export const addPosition = async (position: Position): Promise<Position> => {
  const response: Position = await api<Position>('/vessels/position', {
    method: 'POST',
    body: JSON.stringify(position)
  });
  console.log('\x1b[44m TONIO  addPosition response=', response, '\x1b');
  return response;
};

export const getAllPositions = async (): Promise<Position[]> => {
  const response: Position[] = await api<Position[]>('/vessels/positions', {
    method: 'GET'
  });
  console.log('\x1b[44m TONIO  getAllPositions response=', response, '\x1b');
  return response;
};
