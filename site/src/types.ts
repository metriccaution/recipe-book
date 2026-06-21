export interface Ingredient {
  quantity: string;
  ingredient: string;
  notes?: string;
}

export interface IngredientGroup {
  group?: string;
  ingredients: Ingredient[];
}

export interface InstructionStep {
  text: string;
  substeps?: InstructionStep[];
}

export interface StepGroup {
  title?: string;
  text?: string;
  steps: InstructionStep[];
}

export type Source =
  | { type: 'url'; url: string; description?: string }
  | { type: 'isbn'; isbn: string; page?: number; description?: string }
  | { type: 'described'; description: string };

export interface Recipe {
  identifier: string;
  title: string;
  section: string;
  slug: string;
  created_at: string;
  tags: string[];
  equipment: string[];
  serves?: number;
  prepTime?: string;
  cookingTime?: string;
  source: Source;
  description?: string;
  ingredients: IngredientGroup[];
  steps: StepGroup[];
}
