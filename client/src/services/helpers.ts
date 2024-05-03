import type { Position } from '@/models/vessel';

export const isNumeric = (value: any): boolean => {
  return !isNaN(value - parseFloat(value));
};

export const getRandomInt = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

const allHtmlColorCodeAvailable: string[] = [
  '#F5B7B1',
  '#F1C40F',
  '#FF7F50',
  '#82E0AA',
  '#7B241C',
  '#633974',
  '#145A32',
  '#34495E'
];

export const getHtmlColorCodeForNumber = (num: number): string => {
  const indexMatchingColorCode: number = num % allHtmlColorCodeAvailable.length;
  return allHtmlColorCodeAvailable[indexMatchingColorCode];
};

export const isValidLatitude = (latitude: string | number): boolean => {
  const latitudeAsNumber: number = +latitude;
  return isNumeric(latitudeAsNumber) && latitudeAsNumber >= -90 && latitudeAsNumber <= 90;
};

export const isValidLongitude = (longitude: string | number): boolean => {
  const longitudeAsNumber: number = +longitude;
  return isNumeric(longitudeAsNumber) && longitudeAsNumber >= -180 && longitudeAsNumber <= 180;
};

export const sortPositionsByTimestamp = (positionsToSort: Position[]): Position[] => {
  return [...positionsToSort].sort((p1: Position, p2: Position): number => {
    return p1.createdAt > p2.createdAt ? 1 : -1;
  });
};

// export const waitForGoogleMapToBeLoaded;
