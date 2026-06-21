import { parse, parseInline } from 'marked';

export function md(text: string): string {
  return parseInline(text) as string;
}

export function mdBlock(text: string): string {
  return parse(text) as string;
}

export function siteUrl(path: string): string {
  const base = (import.meta.env.BASE_URL ?? '').replace(/\/$/, '');
  const normPath = path.startsWith('/') ? path : '/' + path;
  return base + normPath;
}

export function slugify(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function parseSingle(iso: string): { hours: number; minutes: number } {
  const hours = parseInt(iso.match(/(\d+)H/)?.[1] ?? '0');
  const minutes = parseInt(iso.match(/(\d+)M/)?.[1] ?? '0');
  return { hours, minutes };
}

function formatPart({ hours, minutes }: { hours: number; minutes: number }): string {
  const parts: string[] = [];
  if (hours) parts.push(`${hours}h`);
  if (minutes) parts.push(`${minutes}m`);
  return parts.join(' ');
}

export function formatDate(iso: string): string {
  const [year, month, day] = iso.split('-').map(Number);
  return new Date(year, month - 1, day).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

export function formatDuration(iso: string | null | undefined): string {
  if (!iso) return '';
  // Handle ranges like PT30M-PT45M (two durations separated by -)
  const rangeMatch = iso.match(/^(PT[^-]+)-(PT.+)$/);
  if (rangeMatch) {
    return `${formatPart(parseSingle(rangeMatch[1]))}–${formatPart(parseSingle(rangeMatch[2]))}`;
  }
  return formatPart(parseSingle(iso));
}
