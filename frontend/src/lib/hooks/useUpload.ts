"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { uploadTransactions } from "@/lib/api/transactions";

export function useUpload() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => uploadTransactions(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });
}
