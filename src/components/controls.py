import customtkinter as ctk

def create_controls(parent, browse_command, baseline_command,
                    verify_command, demo_command, reset_command):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=30, pady=8)

    ctk.CTkButton(
        frame, text="Select Directory", command=browse_command,
        width=140, height=42, corner_radius=10
    ).pack(side="left")

    ctk.CTkButton(
        frame, text="Create Baseline", command=baseline_command,
        width=135, height=42, corner_radius=10
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        frame, text="Verify Integrity", command=verify_command,
        width=135, height=42, corner_radius=10
    ).pack(side="left")

    ctk.CTkButton(
        frame, text="Demo Changes", command=demo_command,
        width=125, height=42, corner_radius=10
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        frame, text="Reset", command=reset_command,
        width=90, height=42, corner_radius=10,
        fg_color="#3b3f46", hover_color="#4b5058"
    ).pack(side="right")
