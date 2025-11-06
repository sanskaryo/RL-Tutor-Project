"use client";

import React, { useState } from "react";
import { cn } from "@/lib/utils"; // ✅ you already have this in /lib/utils.ts
import { AnimatePresence, motion } from "framer-motion"; // ✅ use framer-motion, not motion/react

/**
 * HoverEffect component
 * Displays a grid of hoverable cards with smooth animated background effects.
 */
export const HoverEffect = ({
  items,
  className,
}: {
  items: { title: string; description: string; link?: string }[];
  className?: string;
}) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  return (
    <div
      className={cn(
        "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 py-10",
        className
      )}
    >
      {items.map((item, idx) => (
        <div
          key={idx}
          className="relative group block p-2 h-full w-full cursor-pointer"
          onMouseEnter={() => setHoveredIndex(idx)}
          onMouseLeave={() => setHoveredIndex(null)}
        >
          <AnimatePresence>
            {hoveredIndex === idx && (
              <motion.span
                layoutId="hoverBackground"
                className="absolute inset-0 h-full w-full bg-slate-800/80 rounded-3xl"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1, transition: { duration: 0.15 } }}
                exit={{ opacity: 0, transition: { duration: 0.15, delay: 0.1 } }}
              />
            )}
          </AnimatePresence>

          <Card>
            <CardTitle>{item.title}</CardTitle>
            <CardDescription>{item.description}</CardDescription>
          </Card>
        </div>
      ))}
    </div>
  );
};

/**
 * Card component
 */
export const Card = ({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) => (
  <div
    className={cn(
      "rounded-2xl h-full w-full p-6 overflow-hidden bg-black border border-transparent dark:border-white/[0.2] group-hover:border-slate-700 relative z-20 transition-all duration-300",
      className
    )}
  >
    <div className="relative z-50">{children}</div>
  </div>
);

/**
 * CardTitle component
 */
export const CardTitle = ({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) => (
  <h4
    className={cn(
      "text-white tracking-wide mt-4 text-lg font-semibold",
      className
    )}
  >
    {children}
  </h4>
);

/**
 * CardDescription component
 */
export const CardDescription = ({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) => (
  <p
    className={cn(
      "mt-4 text-gray-400 tracking-wide leading-relaxed text-sm",
      className
    )}
  >
    {children}
  </p>
);
