"use client";

import React from "react";
import { motion } from "motion/react";
import { cn } from "@/lib/utils";

export function MovingBorder({
    children,
    duration = 2000,
    className,
    containerClassName,
    borderClassName,
    as: Component = "button",
    ...otherProps
}: {
    children: React.ReactNode;
    duration?: number;
    className?: string;
    containerClassName?: string;
    borderClassName?: string;
    as?: any;
    [key: string]: any;
}) {
    return (
        <Component
            className={cn(
                "bg-transparent relative text-xl p-[1px] overflow-hidden",
                containerClassName
            )}
            {...otherProps}
        >
            <div
                className="absolute inset-0 rounded-[inherit]"
                style={{
                    padding: "1px",
                }}
            >
                <div className={cn("h-full w-full rounded-[inherit]", borderClassName)}>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        preserveAspectRatio="none"
                        className="absolute h-full w-full"
                        width="100%"
                        height="100%"
                    >
                        <rect
                            fill="none"
                            width="100%"
                            height="100%"
                            rx="inherit"
                            ry="inherit"
                            strokeWidth="2"
                            className="stroke-white/20"
                            style={{
                                strokeDasharray: "200",
                                strokeDashoffset: "200",
                                animation: `dash ${duration}ms linear infinite`,
                            }}
                        />
                    </svg>
                </div>
            </div>

            <div
                className={cn(
                    "relative bg-zinc-950 border border-zinc-800 backdrop-blur-xl text-white flex items-center justify-center w-full h-full text-sm antialiased rounded-[inherit]",
                    className
                )}
            >
                {children}
            </div>
        </Component>
    );
}
