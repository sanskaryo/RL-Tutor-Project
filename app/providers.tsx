"use client";

import React, { useState } from "react";
import { ThemeProvider } from "next-themes";
import {
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

interface RootProvidersProps {
  children: React.ReactNode;
}

const queryClientOptions = {
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 1000 * 30,
    },
    mutations: {
      retry: 1,
    },
  },
};

export function RootProviders({ children }: RootProvidersProps) {
  const [queryClient] = useState(() => new QueryClient(queryClientOptions));

  return (
    <ThemeProvider
      attribute="class"
      themes={["light", "dark", "high-contrast", "system"]}
      defaultTheme="system"
      enableSystem
      storageKey="rl-tutor-theme"
      disableTransitionOnChange
    >
      <QueryClientProvider client={queryClient}>
        {children}
        {process.env.NODE_ENV === "development" ? (
          <ReactQueryDevtools initialIsOpen={false} />
        ) : null}
      </QueryClientProvider>
    </ThemeProvider>
  );
}
