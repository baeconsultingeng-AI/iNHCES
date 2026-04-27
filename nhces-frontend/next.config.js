/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow images from Unsplash and other external sources
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**.supabase.co' },
    ],
  },
};

module.exports = nextConfig;
