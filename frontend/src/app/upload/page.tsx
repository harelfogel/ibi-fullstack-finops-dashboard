"use client";

import { useRouter } from "next/navigation";
import { PageHeader } from "@/components/layout/PageHeader";
import { UploadContent } from "@/components/upload/UploadContent";

export default function UploadPage() {
  const router = useRouter();

  return (
    <div className="mx-auto max-w-4xl">
      <PageHeader
        title="Upload Transactions"
        description="Upload CSV or XLSX files to process and validate transactions."
      />
      <UploadContent onSuccess={() => router.push("/clients")} />
    </div>
  );
}
