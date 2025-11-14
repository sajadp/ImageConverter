import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image
import pillow_heif
import threading
import webbrowser

class ModernImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Format Converter")
        self.root.geometry("900x680")
        self.root.configure(bg='#f3f4f6')
        self.root.resizable(False, True)
        
        # Variables
        self.input_files = []
        self.output_folder = tk.StringVar(value="")
        self.conversion_type = tk.StringVar(value="webp")
        self.quality = tk.IntVar(value=85)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Modern colors
        bg_color = '#f3f4f6'
        card_bg = '#ffffff'
        accent_color = '#0078d4'
        success_color = '#10b981'
        
        # Fonts
        title_font = ('Segoe UI', 18, 'bold')
        subtitle_font = ('Segoe UI', 9)
        section_font = ('Segoe UI', 10, 'bold')
        text_font = ('Segoe UI', 9)
        button_font = ('Segoe UI', 9, 'bold')
        
        # Header
        header = tk.Frame(self.root, bg=accent_color, height=85)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="Image Format Converter", 
                font=title_font, bg=accent_color, fg='white').pack(pady=12)
        tk.Label(header, text="Convert JPG, PNG, HEIC, HEIF to WebP or JPG with high quality", 
                font=subtitle_font, bg=accent_color, fg='#e0e7ff').pack()
        
        # Main container
        container = tk.Frame(self.root, bg=bg_color)
        container.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Left column
        left_col = tk.Frame(container, bg=bg_color)
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right column
        right_col = tk.Frame(container, bg=bg_color)
        right_col.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # === LEFT COLUMN ===
        
        # Input Files Card
        input_card = tk.Frame(left_col, bg=card_bg, relief='flat', bd=0)
        input_card.pack(fill='both', expand=True, pady=(0, 15))
        self._add_shadow(input_card)
        
        tk.Label(input_card, text="Input Files", font=section_font, 
                bg=card_bg, fg='#1f2937').pack(anchor='w', padx=20, pady=(15, 10))
        
        # Buttons row
        btn_frame = tk.Frame(input_card, bg=card_bg)
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        self._create_button(btn_frame, "📁 Select Files", accent_color, 
                           self.select_files).pack(side='left', padx=(0, 8))
        self._create_button(btn_frame, "🗑️ Clear", '#ef4444', 
                           self.clear_files, width=10).pack(side='left')
        
        # Files list
        list_container = tk.Frame(input_card, bg=card_bg)
        list_container.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        list_scroll = tk.Scrollbar(list_container)
        list_scroll.pack(side='right', fill='y')
        
        self.files_listbox = tk.Listbox(list_container, font=text_font,
                                        yscrollcommand=list_scroll.set,
                                        height=8, relief='solid', bd=1,
                                        highlightthickness=0, selectmode='multiple')
        self.files_listbox.pack(side='left', fill='both', expand=True)
        list_scroll.config(command=self.files_listbox.yview)
        
        self.files_count_label = tk.Label(input_card, text="0 files selected",
                                          font=text_font, bg=card_bg, fg='#6b7280')
        self.files_count_label.pack(anchor='w', padx=20, pady=(0, 15))
        
        # Output Folder Card
        output_card = tk.Frame(left_col, bg=card_bg, relief='flat', bd=0)
        output_card.pack(fill='x')
        self._add_shadow(output_card)
        
        tk.Label(output_card, text="Output Folder", font=section_font,
                bg=card_bg, fg='#1f2937').pack(anchor='w', padx=20, pady=(15, 10))
        
        output_frame = tk.Frame(output_card, bg=card_bg)
        output_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        self._create_button(output_frame, "Browse", accent_color,
                           self.select_output_folder, width=10).pack(side='left', padx=(0, 10))
        
        output_entry = tk.Entry(output_frame, textvariable=self.output_folder,
                               font=text_font, relief='solid', bd=1)
        output_entry.pack(side='left', fill='x', expand=True)
        
        # === RIGHT COLUMN ===
        
        # Settings Card
        settings_card = tk.Frame(right_col, bg=card_bg, relief='flat', bd=0)
        settings_card.pack(fill='both', expand=True, pady=(0, 15))
        self._add_shadow(settings_card)
        
        tk.Label(settings_card, text="Conversion Settings", font=section_font,
                bg=card_bg, fg='#1f2937').pack(anchor='w', padx=20, pady=(15, 15))
        
        # Radio buttons
        radio_frame = tk.Frame(settings_card, bg=card_bg)
        radio_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Radiobutton(radio_frame, text="Convert to WebP", 
                      variable=self.conversion_type, value='webp',
                      font=text_font, bg=card_bg, cursor='hand2',
                      activebackground=card_bg, selectcolor=card_bg).pack(anchor='w', pady=3)
        
        tk.Label(radio_frame, text="  Converts JPG, PNG, HEIC, HEIF → WebP",
                font=('Segoe UI', 8), bg=card_bg, fg='#9ca3af').pack(anchor='w', padx=20)
        
        tk.Radiobutton(radio_frame, text="Convert to JPG",
                      variable=self.conversion_type, value='jpg',
                      font=text_font, bg=card_bg, cursor='hand2',
                      activebackground=card_bg, selectcolor=card_bg).pack(anchor='w', pady=(10, 3))
        
        tk.Label(radio_frame, text="  Converts HEIC, HEIF → JPG",
                font=('Segoe UI', 8), bg=card_bg, fg='#9ca3af').pack(anchor='w', padx=20)
        
        # Quality slider
        tk.Label(settings_card, text="Quality", font=section_font,
                bg=card_bg, fg='#1f2937').pack(anchor='w', padx=20, pady=(15, 5))
        
        quality_frame = tk.Frame(settings_card, bg=card_bg)
        quality_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        quality_slider = tk.Scale(quality_frame, from_=1, to=100,
                                 orient='horizontal', variable=self.quality,
                                 command=self.update_quality_label,
                                 bg=card_bg, font=text_font, cursor='hand2',
                                 showvalue=False, highlightthickness=0)
        quality_slider.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.quality_value_label = tk.Label(quality_frame, text="85%",
                font=('Segoe UI', 10, 'bold'), bg=card_bg, fg=accent_color, width=5)
        self.quality_value_label.pack(side='right')
        
        # Convert Button
        convert_btn = tk.Button(right_col, text="🚀 Start Conversion",
                               font=('Segoe UI', 11, 'bold'), bg=success_color,
                               fg='white', cursor='hand2', relief='flat',
                               pady=12, command=self.start_conversion)
        convert_btn.pack(fill='x', pady=(0, 15))
        self._add_shadow(convert_btn)
        
        # Progress Card
        progress_card = tk.Frame(right_col, bg=card_bg, relief='flat', bd=0)
        progress_card.pack(fill='x')
        self._add_shadow(progress_card)
        
        tk.Label(progress_card, text="Progress", font=section_font,
                bg=card_bg, fg='#1f2937').pack(anchor='w', padx=20, pady=(15, 10))
        
        self.progress_var = tk.DoubleVar()
        style = ttk.Style()
        style.configure("Custom.Horizontal.TProgressbar", thickness=20)
        
        self.progress_bar = ttk.Progressbar(progress_card, variable=self.progress_var,
                                           maximum=100, mode='determinate',
                                           style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill='x', padx=20, pady=(0, 10))
        
        self.status_label = tk.Label(progress_card, text="Ready to convert",
                                    font=text_font, bg=card_bg, fg='#6b7280')
        self.status_label.pack(anchor='w', padx=20, pady=(0, 15))
        
        # === FOOTER ===
        footer = tk.Frame(self.root, bg=bg_color, height=40)
        footer.pack(fill='x', side='bottom', pady=(5, 10))
        footer.pack_propagate(False)

        # Center container for footer content
        footer_content = tk.Frame(footer, bg=bg_color)
        footer_content.place(relx=0.5, rely=0.5, anchor='center')

        footer_text = tk.Label(footer_content, text="Made with ", 
                      font=('Segoe UI', 9), bg=bg_color, fg='#6b7280')
        footer_text.pack(side='left')

        heart = tk.Label(footer_content, text="💙", font=('Segoe UI', 11), bg=bg_color)
        heart.pack(side='left')

        by_text = tk.Label(footer_content, text=" by ", 
                  font=('Segoe UI', 9), bg=bg_color, fg='#6b7280')
        by_text.pack(side='left')

        link = tk.Label(footer_content, text="Sajad Parvaneh AI Studio", 
               font=('Segoe UI', 9, 'underline'), bg=bg_color, 
               fg='#0078d4', cursor='hand2')
        link.pack(side='left')
        link.bind("<Button-1>", lambda e: webbrowser.open("https://sajadparvaneh.ir/donate/"))

    
    def _add_shadow(self, widget):
        """Add subtle shadow effect"""
        widget.configure(highlightbackground='#e5e7eb', highlightthickness=1)
    
    def _create_button(self, parent, text, color, command, width=14):
        """Create styled button"""
        return tk.Button(parent, text=text, font=('Segoe UI', 9, 'bold'),
                        bg=color, fg='white', cursor='hand2', relief='flat',
                        width=width, pady=8, command=command)
    
    def update_quality_label(self, value):
        self.quality_value_label.config(text=f"{int(float(value))}%")
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.heic *.heif *.HEIC *.HEIF *.JPG *.JPEG *.PNG"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            for file in files:
                if file not in self.input_files:
                    self.input_files.append(file)
                    self.files_listbox.insert(tk.END, Path(file).name)
            self.update_files_count()
    
    def clear_files(self):
        self.input_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.update_files_count()
    
    def update_files_count(self):
        count = len(self.input_files)
        self.files_count_label.config(text=f"{count} file{'s' if count != 1 else ''} selected")
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def convert_image(self, input_file, output_path):
        try:
            input_path = Path(input_file)
            
            # Handle HEIC/HEIF files
            if input_path.suffix.lower() in ['.heic', '.heif']:
                heif_file = pillow_heif.read_heif(str(input_path))
                image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            else:
                image = Image.open(input_path)
            
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            output_format = self.conversion_type.get()
            output_file = output_path / f"{input_path.stem}.{output_format}"
            
            if output_format == 'webp':
                image.save(output_file, 'WEBP', quality=self.quality.get(), method=6)
            else:
                image.save(output_file, 'JPEG', quality=self.quality.get(), optimize=True)
            
            return True, output_file.name
        except Exception as e:
            return False, str(e)
    
    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "Please select files to convert!")
            return
        
        output_folder = self.output_folder.get().strip()
        if not output_folder:
            messagebox.showwarning("Warning", "Please select an output folder!")
            return
        
        output_path = Path(output_folder)
        if not output_path.exists():
            try:
                output_path.mkdir(parents=True)
            except:
                messagebox.showerror("Error", "Cannot create output folder!")
                return
        
        if self.conversion_type.get() == 'jpg':
            heic_heif_files = [f for f in self.input_files if Path(f).suffix.lower() in ['.heic', '.heif']]
            if len(heic_heif_files) < len(self.input_files):
                if not messagebox.askyesno("Notice",
                    f"You have selected {len(self.input_files) - len(heic_heif_files)} non-HEIC/HEIF files.\n"
                    "Only HEIC/HEIF files will be converted. Continue?"):
                    return
        
        thread = threading.Thread(target=self.process_conversion, daemon=True)
        thread.start()
    
    def process_conversion(self):
        output_path = Path(self.output_folder.get())
        total_files = len(self.input_files)
        successful = 0
        failed = 0
        skipped = 0
        
        for index, file in enumerate(self.input_files, 1):
            file_path = Path(file)
            
            if self.conversion_type.get() == 'jpg' and file_path.suffix.lower() not in ['.heic', '.heif']:
                skipped += 1
                progress = (index / total_files) * 100
                self.progress_var.set(progress)
                continue
            
            self.status_label.config(text=f"Converting {index}/{total_files}: {file_path.name}")
            
            success, result = self.convert_image(file, output_path)
            
            if success:
                successful += 1
            else:
                failed += 1
            
            progress = (index / total_files) * 100
            self.progress_var.set(progress)
            self.root.update_idletasks()
        
        result_text = f"✅ {successful} successful"
        if failed > 0:
            result_text += f"  ❌ {failed} failed"
        if skipped > 0:
            result_text += f"  ⏭️ {skipped} skipped"
        
        self.status_label.config(text=result_text)
        
        message = f"Conversion completed!\n\n✅ Successful: {successful}"
        if failed > 0:
            message += f"\n❌ Failed: {failed}"
        if skipped > 0:
            message += f"\n⏭️ Skipped: {skipped}"
        
        messagebox.showinfo("Complete", message)
        self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernImageConverter(root)
    root.mainloop()
