module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true, 
  },
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect', 
    },
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',          
    'plugin:react-hooks/recommended',    
    'plugin:jsx-a11y/recommended',       
    'plugin:jest/recommended',         
  ],
  plugins: ['react', 'react-hooks', 'jsx-a11y', 'jest'],
  rules: {
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }], 
    'react/prop-types': 'off',    
    'react/react-in-jsx-scope': 'off', 
    'react/no-unescaped-entities': [
      'error',
      { forbid: ['>', '"', "'", '`'] },
    ], 
  },
};
