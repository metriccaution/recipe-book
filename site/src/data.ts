import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import type { Recipe } from "./types.ts";

// process.cwd() = site/ directory when running `astro build`
const root = resolve(process.cwd());
const raw = readFileSync(resolve(root, "public", "repo.json"), "utf-8");
const repo = JSON.parse(raw) as { recipes: Recipe[] };

export const recipes: Recipe[] = repo.recipes;

export function getJsonLd(title: string): string | null {
  const path = resolve(root, "public", "json_ld", `${title}.json`);
  if (!existsSync(path)) return null;
  return readFileSync(path, "utf-8");
}

export function allSections(): string[] {
  return [...new Set(recipes.map((r) => r.section))].sort();
}

export function allTags(): string[] {
  return [...new Set(recipes.flatMap((r) => r.tags))].sort();
}
