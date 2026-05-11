"use client";

import { useQuery } from "@tanstack/react-query";
import { getInsights } from "@/lib/api/insights";

export function useInsights(clientId: string) {
  return useQuery({
    queryKey: ["insights", clientId],
    queryFn: async () => {
      const res = await getInsights(clientId);
      return res.data!;
    },
    enabled: !!clientId,
  });
}
