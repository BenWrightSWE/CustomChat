import NavBar from "@/components/main/NavBar";
import {Theme} from "@radix-ui/themes";
import {Newsreader, Oswald} from "next/font/google";
import {useEffect, useState} from "react";
import {getAppearanceCookie} from "@/lib/utils/cookies";
import type {Metadata} from "next";

const defaultUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : "http://localhost:3000";

export const metadata: Metadata = {
    metadataBase: new URL(defaultUrl),
    title: "Custom Chat",
    description: "Custom AI chat bots for businesses.",
};

const oswald = Oswald({
  weight: "400",
  variable: "--font-Oswald",
  subsets: ["latin"]

});

const newsreader = Newsreader({
  weight: "300",
  variable: "--font-Newsreader",
  subsets: ["latin"],
});


export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  const [appearance, setAppearance] = useState("light");

  useEffect(() => {
    setAppearance(getAppearanceCookie);
  }, []);

  return (
      <Theme appearance={appearance} accentColor={"gold"} className={`${oswald.variable} ${newsreader.variable}`}>
        <header className={"shrink z-50"}>
          <NavBar appearance={appearance} setAppearance={setAppearance}/>
        </header>
        <main>
          {children}
        </main>
        <footer className={""}>

        </footer>
      </Theme>
  );
}
