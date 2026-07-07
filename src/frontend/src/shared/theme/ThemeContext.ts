import React from "react";

export type ThemeName = "light" | "dark" | "print" | "presentation";

export const ThemeContext = React.createContext<{
  theme: ThemeName;
  setTheme: (t: ThemeName) => void;
}>({
  theme: "light",
  setTheme: () => {},
});

export default ThemeContext;
