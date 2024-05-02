export const isNumeric = (value: any): boolean => {
  return !isNaN(value - parseFloat(value));
};
