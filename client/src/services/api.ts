import type { Position } from '@/models/vessel';

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

  const fullUrl: string = url.startsWith('http') ? url : import.meta.env.VITE_BASE_URL + url;
  const response: Response = await fetch(fullUrl, params);
  const json: any = (await response.json()) || {};
  if (!response.ok) {
    const errorMessage = json.details || response.status;
    console.error(response, `  details=${errorMessage}`);
    return Promise.reject(errorMessage);
  }
  return json as T;
};

export const savePosition = async (position: Position): Promise<Position> => {
  return await api<Position>('/vessels/position', {
    method: 'POST',
    body: JSON.stringify(position)
  });
};

export const savePositionsInBulk = async (positions: Position[]): Promise<Position[]> => {
  return await api<Position[]>('/vessels/positions', {
    method: 'POST',
    body: JSON.stringify(positions)
  });
};

export const retrieveAllPositions = async (): Promise<Position[]> => {
  return await api<Position[]>('/vessels/positions', {
    method: 'GET'
  });
};

export const deleteAllPositions = async (): Promise<void> => {
  return await api<void>('/vessels/positions', {
    method: 'DELETE'
  });
};
