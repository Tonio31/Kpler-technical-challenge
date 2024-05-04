import type {
  LatLng,
  Position,
  PositionAndTimeFilter,
  PositionsPerVessel,
  TimeFilter,
  VesselPath
} from '@/models/vessel';
import { getHtmlColorCodeForNumber, sortPositionsByTimestamp } from '@/services/helpers';

export const filterVesselPath = (
  vesselPathToFilter: VesselPath[],
  vesselIdToInclude: string[],
  timeToFilter: TimeFilter | null
): VesselPath[] => {
  const vesselPathFilteredByVesselId: VesselPath[] = vesselPathToFilter.filter(
    (vesselPath: VesselPath): boolean => {
      if (vesselIdToInclude.length === 0) {
        return true;
      } else if (vesselIdToInclude.includes(vesselPath.vesselId)) {
        return true;
      }

      return false;
    }
  );

  if (timeToFilter) {
    return vesselPathFilteredByVesselId.map((vesselPath: VesselPath): VesselPath => {
      return {
        ...vesselPath,
        path: vesselPath.allPositions
          .filter((position: Position) => {
            return position.createdAt < timeToFilter.to;
          })
          .map((position: Position): LatLng => {
            return {
              lat: position.latitude,
              lng: position.longitude
            };
          })
      };
    });
  } else {
    return vesselPathFilteredByVesselId;
  }
};

export const computeVesselPath = (vesselsPositions: PositionsPerVessel): VesselPath[] => {
  const lineSymbol = {
    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
  };

  const vesselPaths: VesselPath[] = [];
  let index: number = 0;
  Object.entries(vesselsPositions).forEach(([vesselId, positions]: [string, Position[]]) => {
    const randomColor: string = getHtmlColorCodeForNumber(index);
    vesselPaths.push({
      vesselId,
      allPositions: positions,
      path: positions.map((position: Position): LatLng => {
        return {
          lat: position.latitude,
          lng: position.longitude
        };
      }),
      icons: [
        {
          icon: lineSymbol,
          offset: '100%'
        }
      ],
      geodesic: true,
      strokeColor: randomColor,
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    index += 1;
  });

  return vesselPaths;
};

export const computeAllTimeFilter = (positionsSorted: Position[]): TimeFilter[] => {
  const earliestDate: number = new Date(positionsSorted[0].createdAt).getTime();
  const latestDate: number = new Date(
    positionsSorted[positionsSorted.length - 1].createdAt
  ).getTime();

  const numberOfStops: number = 50;

  const diffBetweenLatestAndEarliest: number = latestDate - earliestDate;
  const interval: number = diffBetweenLatestAndEarliest / numberOfStops;

  const allTimeFilter: TimeFilter[] = [];
  for (let i: number = 0; i < numberOfStops; i++) {
    allTimeFilter.push({
      from: new Date(earliestDate + i * interval).toISOString(),
      to: new Date(earliestDate + (i + 1) * interval).toISOString()
    });
  }

  return allTimeFilter;
};

export const computePositionsPerVesselAndTimeFilters = (
  positions: Position[]
): PositionAndTimeFilter => {
  const positionsPerVessel: PositionsPerVessel = {};

  const allPositionsSorted: Position[] = sortPositionsByTimestamp(positions);

  const timeFilters: TimeFilter[] = computeAllTimeFilter(allPositionsSorted);

  allPositionsSorted.forEach((position: Position) => {
    if (!positionsPerVessel[position.vesselId]) {
      positionsPerVessel[position.vesselId] = [];
    }

    positionsPerVessel[position.vesselId].push(position);
  });

  return {
    timeFilters,
    positionsPerVessel
  };
};
