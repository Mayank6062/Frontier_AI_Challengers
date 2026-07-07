import React, { useCallback, useEffect, useState } from "react";
import ThemeContext, { ThemeName } from "./ThemeContext";

type Props = { children: React.ReactNode; defaultTheme?: ThemeName };

export function applyThemeStyle(theme: ThemeName, css: string) {
  const id = "og2-theme-tokens";
  let el = document.getElementById(id) as HTMLStyleElement | null;
  if (!el) {
    el = document.createElement("style");
    el.id = id;
    document.head.appendChild(el);
  }
  el.innerHTML = css;
}

export const ThemeProvider = ({ children, defaultTheme = "light" }: Props) => {
  const [theme, setTheme] = useState<ThemeName>(defaultTheme);

  const setThemeAndApply = useCallback((t: ThemeName) => {
    setTheme(t);
    // attempt to fetch built CSS injected at build time as global
    const globalKey = `OG2_TOKENS_CSS_${t.toUpperCase()}`;
    // @ts-ignore
    const css = (window as any)[globalKey] || "";
    if (css) applyThemeStyle(t, css);
  }, []);

  useEffect(() => {
    setThemeAndApply(defaultTheme);
  }, [defaultTheme, setThemeAndApply]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme: setThemeAndApply }}>
      {children}
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
