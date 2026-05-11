"use client";

import { useQuery } from "@tanstack/react-query";
import { getPortfolio } from "@/lib/api/portfolio";

export function usePortfolio(clientId: string) {
  return useQuery({
    queryKey: ["portfolio", clientId],
    queryFn: async () => {
      const res = await getPortfolio(clientId);
      return res.data!;
    },
    enabled: !!clientId,
  });
}
