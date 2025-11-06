export const SUBJECT_COLORS: Record<string, string> = {
  Physics: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  Chemistry: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  Mathematics: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  Biology: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  "Computer Science": "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300",
  All: "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300",
} as const;

export const NODE_TYPES = {
  input: "default",
  output: "output",
  default: "default",
} as const;

export const EDGE_TYPES = {
  default: "default",
  step: "step",
} as const;

export const DEFAULT_NODE_WIDTH = 300;
export const DEFAULT_NODE_HEIGHT = 40;