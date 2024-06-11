import isDate from 'lodash/isDate';

declare global {
  export interface Window {
    panorama: any;
  }
}

const getISOStringFromDate = (date?: Date): string | undefined => (isDate(date) ? date.toISOString() : undefined);

const strHasLength = (str: unknown): str is string => typeof str === 'string' && str.length > 0;

const arrayHasLength = <T>(arr: unknown): arr is T[] => Array.isArray(arr) && arr.length > 0;

const sleep = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

export { getISOStringFromDate, strHasLength, arrayHasLength, sleep };
