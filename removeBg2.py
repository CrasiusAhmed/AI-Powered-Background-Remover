# -*- coding: utf-8 -*-
"""
==============================================================================
|                      AI Background Remover Pro                           |
|----------------------------------------------------------------------------|
|   A user-friendly desktop application to remove backgrounds from images    |
|   with high precision, supporting both single and batch processing.        |
|                                                                            |
|   - Built with Python & CustomTkinter for a modern look and feel.          |
|   - Powered by the 'rembg' library for state-of-the-art results.           |
|                                                                            |
|   -> How to Run:                                                           |
|      1. Make sure you have Python installed.                               |
|      2. Install the required libraries by running this command in your     |
|         terminal or command prompt:                                        |
|         pip install customtkinter rembg Pillow                            |
|      3. Save this code as a Python file (e.g., app.py).                    |
|      4. Run the file from your terminal:                                   |
|         python app.py                                                      |
|                                                                            |
|   -> First Run Note:                                                       |
|      The 'rembg' library will download the required AI model on its first  |
|      use. This is a one-time process and requires an internet connection.  |
|                                                                            |
==============================================================================
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
import io
from rembg import remove

# --- Main Application Class ---
class BackgroundRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        # self.title("A³ Background Remover") # <-- CHANGE YOUR TITLE HERE
        self.title("AI Background Remover")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # --- Set Icon ---
        self._set_application_icon()

        # --- Theme and Appearance ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- App State Variables ---
        self.input_path = ""
        self.output_path = ""
        self.input_folder = ""
        self.output_folder = ""
        self.original_image = None
        self.processed_image = None

        # --- UI Initialization ---
        self._create_widgets()

    def _set_application_icon(self):
        """Sets the application icon."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ico_path = os.path.join(script_dir, "img", "icon.ico")  # Fixed path - ICO is in root, not img folder
            
            if os.path.exists(ico_path):
                self.wm_iconbitmap(ico_path)
        except Exception:
            pass  # Silently ignore icon errors

    def _create_widgets(self):
        """Creates and arranges all the UI elements in the window."""
        
        # --- Configure the main grid layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Top Title Frame ---
        title_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        app_title = ctk.CTkLabel(title_frame, text="AI Background Remover Pro", font=ctk.CTkFont(size=24, weight="bold"))
        app_title.pack()
        
        app_subtitle = ctk.CTkLabel(title_frame, text="Remove backgrounds from images with one click.", font=ctk.CTkFont(size=14), text_color="gray60")
        app_subtitle.pack()

        # --- Tabbed Interface for different modes ---
        self.tab_view = ctk.CTkTabview(self, corner_radius=8)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tab_view.add("Single File")
        self.tab_view.add("Batch Processing")

        # --- Populate Tabs ---
        self._create_single_file_tab()
        self._create_batch_processing_tab()

        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(self, text="Welcome! Select a mode to get started.", anchor="w", font=ctk.CTkFont(size=12))
        self.status_bar.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

    # --- Single File Mode UI and Logic ---
    def _create_single_file_tab(self):
        """Creates the UI for the 'Single File' mode."""
        single_tab = self.tab_view.tab("Single File")
        single_tab.grid_columnconfigure(0, weight=1)
        single_tab.grid_columnconfigure(1, weight=1)
        single_tab.grid_rowconfigure(1, weight=1)

        # --- Top controls frame ---
        controls_frame = ctk.CTkFrame(single_tab, fg_color="transparent")
        controls_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        self.select_button = ctk.CTkButton(controls_frame, text="Select Image", command=self.select_image, height=40)
        self.select_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.save_button = ctk.CTkButton(controls_frame, text="Save Image", command=self.save_image, state="disabled", height=40)
        self.save_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # --- Image display frames ---
        self.original_frame = ctk.CTkFrame(single_tab, border_width=2)
        self.original_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        self.original_frame.grid_propagate(False)
        self.original_frame.grid_columnconfigure(0, weight=1)
        self.original_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self.original_frame, text="Original Image", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=10)
        self.original_image_label = ctk.CTkLabel(self.original_frame, text="")
        self.original_image_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.processed_frame = ctk.CTkFrame(single_tab, border_width=2)
        self.processed_frame.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        self.processed_frame.grid_propagate(False)
        self.processed_frame.grid_columnconfigure(0, weight=1)
        self.processed_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.processed_frame, text="Background Removed", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=10)
        self.processed_image_label = ctk.CTkLabel(self.processed_frame, text="Your result will appear here.")
        self.processed_image_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def select_image(self):
        """Opens a file dialog to select an image and triggers processing."""
        self.input_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All files", "*.*"))
        )
        if not self.input_path:
            return

        self.status_bar.configure(text=f"Selected: {os.path.basename(self.input_path)}")
        self.save_button.configure(state="disabled")
        self.processed_image_label.configure(text="Processing...", image=None)
        
        # Display original image
        try:
            self.original_image = Image.open(self.input_path)
            self.display_image(self.original_image, self.original_image_label)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image file: {e}")
            return

        # Process in a separate thread to keep the UI responsive
        threading.Thread(target=self.process_image, daemon=True).start()

    def process_image(self):
        """Handles the background removal using the 'rembg' library."""
        try:
            self.status_bar.configure(text="Processing... Please wait.")
            # Re-open the file as bytes for rembg
            with open(self.input_path, "rb") as f:
                input_bytes = f.read()
            
            output_bytes = remove(input_bytes)
            
            self.processed_image = Image.open(io.BytesIO(output_bytes))
            
            # Update UI from the main thread
            self.after(0, self.update_processed_image_display)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Processing Error", f"An error occurred: {e}"))
            self.status_bar.configure(text="Error during processing.")

    def update_processed_image_display(self):
        """Updates the UI with the processed image."""
        if self.processed_image:
            self.display_image(self.processed_image, self.processed_image_label)
            self.save_button.configure(state="normal")
            self.status_bar.configure(text="Processing complete! Click 'Save Image'.")

    def save_image(self):
        """Saves the processed image to a location chosen by the user."""
        if not self.processed_image:
            messagebox.showerror("Save Error", "There is no processed image to save.")
            return
        
        self.output_path = filedialog.asksaveasfilename(
            title="Save Processed Image",
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
            initialfile=f"{os.path.splitext(os.path.basename(self.input_path))[0]}_no_bg.png"
        )

        if self.output_path:
            try:
                self.processed_image.save(self.output_path)
                self.status_bar.configure(text=f"Image saved to {self.output_path}")
                messagebox.showinfo("Success", "The image has been saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save the image: {e}")

    def display_image(self, pil_image, label_widget):
        """
        Helper function to load and display a PIL image in a CTkLabel.
        It creates a resized COPY for display, leaving the original intact.
        """
        try:
            # Get container dimensions
            container_width = label_widget.winfo_width()
            container_height = label_widget.winfo_height()
            
            if container_width < 50 or container_height < 50: # Wait for widget to be drawn
                self.after(100, lambda: self.display_image(pil_image, label_widget))
                return

            # *** FIX: Create a copy for displaying, leaving the original untouched ***
            display_copy = pil_image.copy()
            
            # Resize the copy to fit the container while maintaining aspect ratio
            display_copy.thumbnail((container_width - 20, container_height - 20), Image.Resampling.LANCZOS)
            
            # Create the image for CustomTkinter
            ctk_image = ctk.CTkImage(light_image=display_copy, dark_image=display_copy, size=display_copy.size)
            
            # Configure the label with the new image
            label_widget.configure(image=ctk_image, text="")
            # Keep a reference to prevent garbage collection
            label_widget.image = ctk_image

        except Exception as e:
            label_widget.configure(text=f"Error loading image:\n{e}", image=None)


    # --- Batch Processing Mode UI and Logic ---
    def _create_batch_processing_tab(self):
        """Creates the UI for the 'Batch Processing' mode."""
        batch_tab = self.tab_view.tab("Batch Processing")
        batch_tab.grid_columnconfigure(0, weight=1)
        batch_tab.grid_rowconfigure(2, weight=1)

        # --- Folder selection frame ---
        folder_frame = ctk.CTkFrame(batch_tab, fg_color="transparent")
        folder_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        folder_frame.grid_columnconfigure(0, weight=1)
        folder_frame.grid_columnconfigure(1, weight=1)

        self.input_folder_button = ctk.CTkButton(folder_frame, text="Select Input Folder", command=self.select_input_folder, height=40)
        self.input_folder_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.input_folder_label = ctk.CTkLabel(folder_frame, text="No folder selected", text_color="gray60", anchor="w")
        self.input_folder_label.grid(row=1, column=0, padx=0, pady=(5,10), sticky="ew")

        self.output_folder_button = ctk.CTkButton(folder_frame, text="Select Output Folder", command=self.select_output_folder, height=40)
        self.output_folder_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        self.output_folder_label = ctk.CTkLabel(folder_frame, text="No folder selected", text_color="gray60", anchor="w")
        self.output_folder_label.grid(row=1, column=1, padx=10, pady=(5,10), sticky="ew")

        # --- Start button ---
        self.start_batch_button = ctk.CTkButton(batch_tab, text="Start Batch Processing", command=self.start_batch_processing, state="disabled", height=40)
        self.start_batch_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # --- File list / Log view ---
        self.log_textbox = ctk.CTkTextbox(batch_tab, state="disabled", font=ctk.CTkFont(family="monospace"))
        self.log_textbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # --- Progress bar ---
        self.progress_bar = ctk.CTkProgressBar(batch_tab)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

    def select_input_folder(self):
        """Selects the folder containing images to be processed."""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_folder_label.configure(text=f".../{os.path.basename(folder)}")
            self.update_batch_button_state()

    def select_output_folder(self):
        """Selects the folder where processed images will be saved."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_folder_label.configure(text=f".../{os.path.basename(folder)}")
            self.update_batch_button_state()

    def update_batch_button_state(self):
        """Enables the start button only if both folders are selected."""
        if self.input_folder and self.output_folder:
            self.start_batch_button.configure(state="normal")
        else:
            self.start_batch_button.configure(state="disabled")

    def start_batch_processing(self):
        """Starts the batch processing in a new thread."""
        if not self.input_folder or not self.output_folder:
            messagebox.showwarning("Warning", "Please select both an input and an output folder.")
            return
            
        if self.input_folder == self.output_folder:
            messagebox.showwarning("Warning", "Input and Output folders cannot be the same. Please choose a different output folder.")
            return

        self.start_batch_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.configure(state="disabled")
        
        # Run processing in a thread to not freeze the GUI
        threading.Thread(target=self.batch_process_thread, daemon=True).start()

    def batch_process_thread(self):
        """The actual logic for processing files in a folder."""
        try:
            self.status_bar.configure(text="Batch processing started...")
            self.add_log_message("--- Starting Batch Processing ---")
            
            valid_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.bmp']
            files_to_process = [f for f in os.listdir(self.input_folder) if os.path.splitext(f)[1].lower() in valid_extensions]
            
            if not files_to_process:
                self.add_log_message("No valid image files found in the input folder.")
                self.add_log_message("--- Batch Processing Finished ---")
                self.status_bar.configure(text="Batch complete. No images found.")
                self.after(0, lambda: self.start_batch_button.configure(state="normal"))
                return

            total_files = len(files_to_process)
            self.add_log_message(f"Found {total_files} image(s) to process.")

            for i, filename in enumerate(files_to_process):
                input_file_path = os.path.join(self.input_folder, filename)
                output_filename = f"{os.path.splitext(filename)[0]}_no_bg.png"
                output_file_path = os.path.join(self.output_folder, output_filename)
                
                self.add_log_message(f"Processing ({i+1}/{total_files}): {filename}")
                
                try:
                    with open(input_file_path, 'rb') as f_in:
                        with open(output_file_path, 'wb') as f_out:
                            input_data = f_in.read()
                            output_data = remove(input_data)
                            f_out.write(output_data)
                    self.add_log_message(f"  -> Saved to: {output_filename}")
                except Exception as e:
                    self.add_log_message(f"  -> FAILED: {e}")

                # Update progress bar on the main thread
                progress = (i + 1) / total_files
                self.after(0, self.progress_bar.set, progress)

            self.add_log_message("--- Batch Processing Finished ---")
            self.status_bar.configure(text="Batch processing complete!")
            self.after(0, lambda: messagebox.showinfo("Success", "Batch processing has finished successfully!"))

        except Exception as e:
            self.add_log_message(f"An unexpected error occurred: {e}")
            self.status_bar.configure(text="An error occurred during batch processing.")
        finally:
            # Re-enable the button on the main thread
            self.after(0, lambda: self.start_batch_button.configure(state="normal"))

    def add_log_message(self, message):
        """Adds a message to the log text box in a thread-safe way."""
        def _update_log():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", f"{message}\n")
            self.log_textbox.see("end") # Auto-scroll
            self.log_textbox.configure(state="disabled")
        
        # Schedule the UI update on the main thread
        self.after(0, _update_log)


# --- Application Entry Point ---
if __name__ == "__main__":
    # This is required for 'rembg' when using multiprocessing in a frozen app (e.g., PyInstaller)
    import multiprocessing
    multiprocessing.freeze_support()
    
    app = BackgroundRemoverApp()
    app.mainloop()
