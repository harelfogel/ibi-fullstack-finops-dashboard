"use client";

import { useQuery } from "@tanstack/react-query";
import { getViolations } from "@/lib/api/violations";

export function useViolations(clientId: string) {
  return useQuery({
    queryKey: ["violations", clientId],
    queryFn: async () => {
      const res = await getViolations(clientId);
      return res.data!;
    },
    enabled: !!clientId,
  });
}
