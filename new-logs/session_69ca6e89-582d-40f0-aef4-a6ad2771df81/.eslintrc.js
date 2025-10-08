module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: [
    '@typescript-eslint',
    'prettier'
  ],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:prettier/recommended'
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    project: './tsconfig.json', // Specify the tsconfig.json file
  },
  rules: {
    // Override rules here if needed
    '@typescript-eslint/no-explicit-any': 'warn', // Example: Warn about 'any' type
    '@typescript-eslint/no-unused-vars': 'warn', // Warn about unused variables
    'prettier/prettier': ['error', {
      endOfLine: 'lf',
    }],
    // Add other rules as per project standards
  },
  ignorePatterns: ['node_modules/', 'dist/', '*.d.ts'],
};
