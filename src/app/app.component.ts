import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ColorRGB {
  r: number;
  g: number;
  b: number;
}

interface ColorCMYK {
  c: number;
  m: number;
  y: number;
  k: number;
}

interface ColorHSV {
  h: number;
  s: number;
  v: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'KG_lab1';

  currentColor = '#ffffff';
  rgb: ColorRGB = { r: 255, g: 255, b: 255 };
  cmyk: ColorCMYK = { c: 0, m: 0, y: 0, k: 0 };
  hsv: ColorHSV = { h: 0, s: 0, v: 100 };

  rgbError: string | null = null;
  cmykError: string | null = null;
  hsvError: string | null = null;

  paletteColors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff'];

  selectPaletteColor(color: string) {
    this.setColor(color);
  }

  setColor(color: string) {
    try {
      this.clearErrors();
      this.currentColor = color;
      this.rgb = this.hexToRgb(color);
      this.cmyk = this.rgbToCmyk(this.rgb);
      this.hsv = this.rgbToHsv(this.rgb);
    } catch (error) {
      console.error('Ошибка при установке цвета:', error);
      this.setErrors('Ошибка при установке цвета');
    }
  }

  onColorPickerChange(event: any) {
    this.currentColor = event.target.value;
    this.rgb = this.hexToRgb(this.currentColor);
    this.cmyk = this.rgbToCmyk(this.rgb);
    this.hsv = this.rgbToHsv(this.rgb);
  }

  onRgbChange() {
    try {
      this.clearErrors();
      this.rgb = this.checkRgb(this.rgb);
      this.currentColor = this.rgbToHex(this.rgb);
      this.cmyk = this.rgbToCmyk(this.rgb);
      this.hsv = this.rgbToHsv(this.rgb);
    } catch (error) {
      console.error('Ошибка при обновлении цвета:', error);
      this.setErrors('Ошибка при обновлении цвета');
    }
  }

  onCmykChange() {
    try {
      this.clearErrors();
      this.cmyk= this.checkCmyk(this.cmyk)
      this.rgb = this.cmykToRgb(this.cmyk);
      this.hsv = this.rgbToHsv(this.rgb);
      this.currentColor = this.rgbToHex(this.rgb);
    } catch (error) {
      console.error('Ошибка при обновлении цвета:', error);
      this.setErrors('Ошибка при обновлении цвета');
    }
  }

  onHsvChange() {
    try {
      this.clearErrors();
      this.hsv = this.checkHsv(this.hsv);
      this.rgb = this.hsvToRgb(this.hsv);
      this.cmyk = this.rgbToCmyk(this.rgb);
      this.currentColor = this.rgbToHex(this.rgb);
    } catch (error) {
      console.error('Ошибка при обновлении цвета:', error);
      this.setErrors('Ошибка при обновлении цвета');
    }
  }

  rgbToCmyk(rgb: ColorRGB): ColorCMYK {
    try {
      const { r, g, b } = this.rgb;
      const k = 1 - Math.max(r / 255, g / 255, b / 255);

      if (k === 1) {
        return { c: 0, m: 0, y: 0, k: 100 };
      }

      const c = (1 - r / 255 - k) / (1 - k);
      const m = (1 - g / 255 - k) / (1 - k);
      const y = (1 - b / 255 - k) / (1 - k);

      return { c: Math.round(c * 100), m: Math.round(m * 100), y: Math.round(y * 100), k: Math.round(k * 100) };
    } catch (error) {
      console.error('Ошибка при конвертации RGB в CMYK:', error);
      return { c: 0, m: 0, y: 0, k: 0 };
    }
  }

  cmykToRgb(cmyk: ColorCMYK): ColorRGB {
    try {
      const { c, m, y, k } = this.cmyk;
      const r = 255 * (1 - c / 100) * (1 - k / 100);
      const g = 255 * (1 - m / 100) * (1 - k / 100);
      const b = 255 * (1 - y / 100) * (1 - k / 100);
      return { r: Math.round(r), g: Math.round(g), b: Math.round(b) };
    } catch (error) {
      console.error('Ошибка при конвертации CMYK в RGB:', error);
      return { r: 0, g: 0, b: 0 };
    }
  }

  rgbToHsv(rgb: ColorRGB): ColorHSV {
    try {
      const { r, g, b } = this.rgb;
      const max = Math.max(r, g, b);
      const min = Math.min(r, g, b);
      let h = 0, s, v = max;

      const d = max - min;
      s = max === 0 ? 0 : (d / max) * 100;

      if (max === min) {
        h = 0;
      } else {
        switch (max) {
          case r:
            h = (g - b) / d + (g < b ? 6 : 0);
            break;
          case g:
            h = (b - r) / d + 2;
            break;
          case b:
            h = (r - g) / d + 4;
            break;
        }
        h *= 60;
      }

      return { h: Math.round(h), s: Math.round(s), v: Math.round((v / 255) * 100) };
    } catch (error) {
      console.error('Ошибка при конвертации RGB в HSV:', error);
      return { h: 0, s: 0, v: 0 };
    }
  }

  hsvToRgb(hsv: ColorHSV): ColorRGB {
    try {
      const { h, s, v } = this.hsv;
      const c = (v * s) / 10000;
      const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
      const m = (v / 100) - c;
      let r = 0, g = 0, b = 0;

      if (h >= 0 && h < 60) {
        r = c;
        g = x;
      } else if (h >= 60 && h < 120) {
        r = x;
        g = c;
      } else if (h >= 120 && h < 180) {
        g = c;
        b = x;
      } else if (h >= 180 && h < 240) {
        g = x;
        b = c;
      } else if (h >= 240 && h < 300) {
        r = x;
        b = c;
      } else {
        r = c;
        b = x;
      }

      return {
        r: Math.round((r + m) * 255),
        g: Math.round((g + m) * 255),
        b: Math.round((b + m) * 255)
      };
    } catch (error) {
      console.error('Ошибка при конвертации HSV в RGB:', error);
      return { r: 0, g: 0, b: 0 };
    }
  }

  rgbToHex(rgb: ColorRGB): string {
    try {
      const { r, g, b } = this.rgb;
      const rHex = r.toString(16).padStart(2, '0');
      const gHex = g.toString(16).padStart(2, '0');
      const bHex = b.toString(16).padStart(2, '0');
      return `#${rHex}${gHex}${bHex}`;
    } catch (error) {
      console.error('Ошибка при конвертации RGB в HEX:', error);
      return '#000000';
    }
  }

  hexToRgb(hex: string): ColorRGB {
    try {
      if (!this.isValidHex(hex)) {
        throw new Error('Недопустимый формат шестнадцатеричного цвета');
      }
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      return { r, g, b };
    } catch (error) {
      console.error('Ошибка при конвертации HEX в RGB:', error);
      return { r: 0, g: 0, b: 0 };
    }
  }

  checkRgb(rgb: ColorRGB): ColorRGB {
    const { r, g, b } = rgb;

    if (r == null || g == null || b == null) {
      this.rgbError = 'Отсутствие некоторых значений RGB, используется 0';
      return { r: 0, g: 0, b: 0 }; 
    }

    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
      this.rgbError = 'Некорректные значения RGB, используется ближайшая граница';
      return { r: Math.max(0, Math.min(r, 255)), g: Math.max(0, Math.min(g, 255)), b: Math.max(0, Math.min(b, 255)) };
    }
    return rgb;
  }

  checkCmyk(cmyk: ColorCMYK): ColorCMYK {
    const { c, m, y, k } = cmyk;

    if (c == null || m == null || y == null || k == null) {
      this.cmykError = 'Отсутствие некоторых значений CMYK, используется 0';
      return { c: 0, m: 0, y: 0, k: 0}; 
    }

    if (c < 0 || c > 100 || m < 0 || m > 100 || y < 0 || y > 100 || k < 0 || k > 100) {
      this.cmykError = 'Некорректные значения CMYK, используется ближайшая граница';
      return { c: Math.max(0, Math.min(c, 100)), m: Math.max(0, Math.min(m, 100)), y: Math.max(0, Math.min(y, 100)), k: Math.max(0, Math.min(k, 100)) };
    }
    return cmyk;
  }

  checkHsv(hsv: ColorHSV): ColorHSV {
    const { h, s, v } = hsv;

    if (h == null || s == null || v == null) {
      this.hsvError = 'Отсутствие некоторых значений HSV, используется 0';
      return { h: 0, s: 0, v: 0 }; 
    }

    if (h < 0 || h > 360 || s < 0 || s > 100 || v < 0 || v > 100) {
      this.hsvError = 'Некорректные значения HSV, используется ближайшая граница';
      return { h: Math.max(0, Math.min(h, 360)), s: Math.max(0, Math.min(s, 100)), v: Math.max(0, Math.min(v, 100)) };
    }
    return hsv;
  }

  isValidHex(hex: string): boolean {
    return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex);
  }

  private clearErrors() {
    this.rgbError = null;
    this.cmykError = null;
    this.hsvError = null;
  }

  private setErrors(errorMessage: string) {
    this.rgbError = errorMessage;
    this.cmykError = errorMessage;
    this.hsvError = errorMessage;
  }
}