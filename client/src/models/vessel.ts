export interface Position {
  createdAt: string;
  id?: number;
  latitude: number;
  longitude: number;
  vesselId: number;
}

export const VESSEL_ID_QUERY_PARAM_KEY: string = 'vesselIds' as const;

export type LatLng = google.maps.LatLngLiteral;

export interface VesselPath extends google.maps.PolylineOptions {
  vesselId: string;
  allPositions: Position[];
}

export interface PositionsPerVessel {
  [vesselId: string]: Position[];
}

export interface IsItWaterApiResponse {
  longitude: string;
  latitude: string;
  water: boolean;
}

export interface TimeFilter {
  from: string;
  to: string;
}

export interface PositionAndTimeFilter {
  timeFilters: TimeFilter[];
  positionsPerVessel: PositionsPerVessel;
}
