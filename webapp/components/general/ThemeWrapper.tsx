'use client'

import { Theme } from "@radix-ui/themes";
import { oswald, newsreader } from "@/lib/utils/fonts";
import { useAppearance } from "@/lib/contexts/AppearanceContext"

interface ThemeWrapperProps {
    children: React.ReactNode;
    fonts?: {
        header?: boolean;
        body?: boolean;
    }
}

export default function ThemeWrapper({ children, fonts = {header: true, body: true}}: ThemeWrapperProps) {
    const { appearance } = useAppearance();

    const fontClasses = [
        fonts?.header && oswald.variable,
        fonts?.body && newsreader.variable
    ].filter(Boolean).join('');

    return (
        <Theme appearance={appearance} accentColor={"gold"} className={fontClasses}>
            {children}
        </Theme>
    );
}