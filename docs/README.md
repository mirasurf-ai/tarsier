# Tarsier Landing Page

This is the static landing page for the Tarsier project, built with Jekyll.

## Setup

1. Install Ruby and Jekyll:
   ```bash
   gem install jekyll bundler
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Build and serve the site:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser to `http://localhost:4000`

## Deployment

To deploy to GitHub Pages:
1. Push this repository to GitHub
2. Go to repository Settings > Pages
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/docs" folder
5. Your site will be available at `https://yourusername.github.io/repository-name/`

## Project Structure

- `index.html` - Main landing page
- `_config.yml` - Jekyll configuration
- `_layouts/` - Page templates
- `_includes/` - Reusable components
- `Gemfile` - Ruby dependencies

The landing page showcases:
- **TarsierOCR** - High-performance optical recognition using advanced visual LLM models
- **TarsierSearch** - Web and in-app search liberation for LLM and AI
- **TarsierSone** - Agent audio processing and communication capabilities
- Future modules and expansion plans

## Features

- Responsive design
- Modern CSS animations
- SEO optimized
- Social media meta tags
- Clean, professional layout 