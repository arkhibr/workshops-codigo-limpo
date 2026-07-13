import { defineConfig } from "vitest/config";

// Os arquivos deste workshop seguem a convenção de nomes do repositório
// (equivalente.ts, exercicio.ts, gabarito.ts) em vez do padrão *.test.ts/*.spec.ts
// do Vitest. O include abaixo cobre ambos os padrões.
export default defineConfig({
  test: {
    include: [
      "**/*.{test,spec}.?(c|m)[jt]s?(x)",
      "**/tutorial-*/**/{equivalente,exercicio,gabarito}.ts",
    ],
  },
});
