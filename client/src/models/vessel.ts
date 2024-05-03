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
}

export interface PositionsPerVessel {
  [vesselId: string]: Position[];
}

export interface IsItWaterApiResponse {
  longitude: string;
  latitude: string;
  water: boolean;
}
