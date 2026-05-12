"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteClient } from "@/lib/api/clients";

export function useDeleteClient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (clientId: string) => deleteClient(clientId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });
}
