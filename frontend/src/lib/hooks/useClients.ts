"use client";

import { useQuery } from "@tanstack/react-query";
import { getClients } from "@/lib/api/clients";

export function useClients() {
  return useQuery({
    queryKey: ["clients"],
    queryFn: async () => {
      const res = await getClients();
      return res.data!;
    },
  });
}
