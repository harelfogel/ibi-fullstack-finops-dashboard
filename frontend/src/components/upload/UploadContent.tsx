"use client";

import { useState } from "react";
import { FileDropZone } from "@/components/upload/FileDropZone";
import { ValidationSummary } from "@/components/upload/ValidationSummary";
import { ErrorTable } from "@/components/upload/ErrorTable";
import { Card } from "@/components/ui/Card";
import { Spinner } from "@/components/ui/Spinner";
import { useUpload } from "@/lib/hooks/useUpload";
import { useToast } from "@/lib/providers/ToastProvider";
import type { UploadResult } from "@/types/transaction";

interface UploadContentProps {
  onSuccess?: (result: UploadResult) => void;
  compact?: boolean;
}

export function UploadContent({ onSuccess, compact }: UploadContentProps) {
  const upload = useUpload();
  const { addToast } = useToast();
  const [result, setResult] = useState<UploadResult | null>(null);

  const handleFileSelect = async (file: File) => {
    setResult(null);
    try {
      const response = await upload.mutateAsync(file);
      if (response.data) {
        setResult(response.data);
        if (response.data.error_rows === 0) {
          addToast("success", `Successfully processed ${response.data.valid_rows} transactions`);
        } else {
          addToast(
            "info",
            `Processed ${response.data.valid_rows} valid, ${response.data.error_rows} errors`,
          );
        }
        onSuccess?.(response.data);
      }
    } catch (err) {
      addToast("error", err instanceof Error ? err.message : "Upload failed");
    }
  };

  return (
    <div className={compact ? "space-y-4" : "space-y-6"}>
      <Card className={compact ? "p-4" : undefined}>
        <FileDropZone
          onFileSelect={handleFileSelect}
          disabled={upload.isPending}
        />
        {upload.isPending && (
          <div className="mt-4 flex items-center gap-2 text-sm text-slate-400">
            <Spinner />
            <span>Processing file...</span>
          </div>
        )}
      </Card>

      {result && (
        <>
          <ValidationSummary result={result} />
          {result.errors.length > 0 && (
            <div>
              <h2 className="mb-3 text-lg font-semibold text-white">
                Validation Errors
              </h2>
              <ErrorTable errors={result.errors} />
            </div>
          )}
          {result.affected_clients.length > 0 && (
            <Card>
              <h3 className="mb-2 text-sm font-medium text-slate-400">
                Affected Clients
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.affected_clients.map((id) => (
                  <span
                    key={id}
                    className="rounded-lg bg-cyan-500/10 px-3 py-1 text-sm font-mono text-cyan-400"
                  >
                    {id}
                  </span>
                ))}
              </div>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
