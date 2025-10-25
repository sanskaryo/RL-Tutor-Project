import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind classes conditionally.
 * Usage: cn("px-2", isActive && "bg-black", "px-4") // -> "bg-black px-4"
 */
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}
