import { Inter } from "next/font/google";
import Navbar from "@/components/Navbar";
import UpgradeModal from "@/components/UpgradeModal";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "AI Resume Coach - Build ATS-Optimized Resumes",
  description: "Transform ordinary resume bullet points into compelling professional achievements. Get hired faster with AI-optimized content.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        <UpgradeModal />
        {children}
      </body>
    </html>
  );
}
