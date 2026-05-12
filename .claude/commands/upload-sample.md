Upload the sample CSV file and report results.

Steps:
1. Verify the backend is running: `curl -s http://localhost:8000/health`.
2. Upload the sample file:
   ```
   curl -s -X POST http://localhost:8000/api/v1/transactions/upload \
     -F "file=@sample_data/transactions_sample.csv"
   ```
3. Parse and display the JSON response:
   - Total rows processed
   - Valid rows inserted
   - Error rows (if any) with details
   - Affected client IDs
   - Batch ID
4. Verify downstream effects:
   - `curl -s http://localhost:8000/api/v1/clients` — list clients created
   - Pick the first client and show their portfolio and violations
5. Report a summary of the upload pipeline results.
