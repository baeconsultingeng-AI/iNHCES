'use client';
import { useEffect, useState } from 'react';
import { GS, COLOURS } from '@/lib/styles';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { listReports, type Report } from '@/lib/api';
import { formatDate, formatDateTime } from '@/lib/formatters';
import Link from 'next/link';

function ReportRow({ report, index }: { report: Report; index: number }) {
  const [downloading, setDownloading] = useState(false);
  const isExpired = report.url_expires_at
    ? new Date(report.url_expires_at) < new Date()
    : true;

  async function handleDownload() {
    if (!report.download_url) { alert('No download URL — regenerate the report.'); return; }
    setDownloading(true);
    window.open(report.download_url, '_blank');
    setTimeout(() => setDownloading(false), 1500);
  }

  return (
    <tr style={{ background: index % 2 === 0 ? COLOURS.surface : COLOURS.surfaceAlt }}>
      <td style={GS.td}>
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 13, color: COLOURS.textMuted }}>
          {report.project_id.slice(0, 8)}...
        </span>
      </td>
      <td style={GS.td}>
        <span style={{ fontFamily: 'var(--font-ui)', fontSize: 13, color: COLOURS.textPrimary }}>
          {formatDate(report.created_at)}
        </span>
        <p style={{ ...GS.metaText, margin: 0, fontSize: 11 }}>
          {formatDateTime(report.created_at)}
        </p>
      </td>
      <td style={GS.td}>
        {report.page_count && (
          <span style={{ fontFamily: 'var(--font-ui)', fontSize: 13 }}>
            {report.page_count} pages
          </span>
        )}
        {report.file_size_bytes && (
          <p style={{ ...GS.metaText, margin: 0, fontSize: 11 }}>
            {(report.file_size_bytes / 1024).toFixed(1)} KB
          </p>
        )}
      </td>
      <td style={GS.td}>
        {isExpired ? (
          <span style={{ ...GS.metaText, fontSize: 12, color: COLOURS.amber }}>
            URL expired
          </span>
        ) : (
          <span style={{ ...GS.metaText, fontSize: 12, color: COLOURS.green }}>
            Valid until {report.url_expires_at?.slice(0, 10)}
          </span>
        )}
      </td>
      <td style={{ ...GS.td, textAlign: 'right' }}>
        <Button
          variant="ghost"
          size="sm"
          loading={downloading}
          onClick={handleDownload}
          style={{ fontSize: 12 }}
        >
          Download PDF
        </Button>
      </td>
    </tr>
  );
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState<string | null>(null);

  useEffect(() => {
    listReports()
      .then(r => setReports(r.items))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ ...GS.page, paddingTop: 40 }}>
      <div style={{ ...GS.spaceBetween, marginBottom: 32 }} className="anim">
        <div>
          <h1 style={GS.pageTitle}>Reports</h1>
          <p style={GS.pageSub}>
            Your generated PDF cost reports. Download links refresh automatically.
          </p>
        </div>
        <Link href="/estimate">
          <Button>New Estimate</Button>
        </Link>
      </div>

      {loading && <LoadingSpinner label="Loading reports..." />}

      {error && (
        <div style={{ ...GS.alertInfo, marginBottom: 24 }}>
          <strong>Log in to view your reports.</strong>
          <p style={{ margin: '4px 0 0', fontSize: 13 }}>
            PDF reports are linked to your account. Log in or create an account to access them.
          </p>
        </div>
      )}

      {!loading && !error && reports.length === 0 && (
        <Card style={{ textAlign: 'center', padding: 48 }}>
          <p style={{ fontFamily: 'var(--font-display)', fontSize: 20, color: COLOURS.textDim, margin: '0 0 8px' }}>
            No reports yet
          </p>
          <p style={{ ...GS.metaText, marginBottom: 20 }}>
            Generate a cost estimate first, then click &ldquo;Generate PDF Report&rdquo;.
          </p>
          <Link href="/estimate">
            <Button>Get an Estimate</Button>
          </Link>
        </Card>
      )}

      {reports.length > 0 && (
        <Card style={{ padding: 0, overflow: 'hidden' }} className="anim">
          <table style={GS.table}>
            <thead>
              <tr>
                <th style={GS.th}>Project ID</th>
                <th style={GS.th}>Date Generated</th>
                <th style={GS.th}>Size</th>
                <th style={GS.th}>Download Link</th>
                <th style={{ ...GS.th, textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((r, i) => (
                <ReportRow key={r.id} report={r} index={i} />
              ))}
            </tbody>
          </table>
          <p style={{ ...GS.metaText, padding: '10px 16px', fontSize: 11 }}>
            {reports.length} report{reports.length !== 1 ? 's' : ''}. Download links expire after 24 hours and are auto-refreshed on page load.
          </p>
        </Card>
      )}
    </div>
  );
}
