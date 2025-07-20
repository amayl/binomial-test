import customtkinter as ctk
from tkinter import messagebox

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

"""STATS ENGINE"""
def factorial(n: int):
    if n <= 1:
        return 1
    else:
        result = 1
        for i in range(1, n+1):
            result *= i
        return result

def binomial_dist(n: int, p: float, x: int):
    nCx = factorial(n) / (factorial(x) * factorial(n - x))
    return nCx * (p ** x) * ((1 - p) ** (n - x))

def cdf(n: int, p: float, x: int):
    probability = 0
    for i in range(0, x + 1):
        probability = probability + binomial_dist(n, p, i)
    return probability

class StatsEngineApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Binomial Hypothesis Test Engine")
        self.geometry("800x700")
        self.minsize(600, 500)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Binomial Hypothesis Test", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Test type selection
        self.test_type_label = ctk.CTkLabel(self.main_frame, text="Test Type:", font=ctk.CTkFont(size=16, weight="bold"))
        self.test_type_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")

        self.test_type_var = ctk.StringVar(value="1-tail")
        self.test_type_frame = ctk.CTkFrame(self.main_frame)
        self.test_type_frame.grid(row=1, column=1, padx=20, pady=(10, 5), sticky="ew")

        self.one_tail_radio = ctk.CTkRadioButton(
            self.test_type_frame, 
            text="1-Tailed Test", 
            variable=self.test_type_var, 
            value="1-tail",
            command=self.on_test_type_change
        )
        self.one_tail_radio.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.two_tail_radio = ctk.CTkRadioButton(
            self.test_type_frame, 
            text="2-Tailed Test", 
            variable=self.test_type_var, 
            value="2-tail",
            command=self.on_test_type_change
        )
        self.two_tail_radio.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Direction selection (for 1-tailed tests)
        self.direction_label = ctk.CTkLabel(self.main_frame, text="Direction:", font=ctk.CTkFont(size=16, weight="bold"))
        self.direction_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")

        self.direction_var = ctk.StringVar(value="greater")
        self.direction_frame = ctk.CTkFrame(self.main_frame)
        self.direction_frame.grid(row=2, column=1, padx=20, pady=(10, 5), sticky="ew")

        self.greater_radio = ctk.CTkRadioButton(
            self.direction_frame, 
            text="Greater than (>)", 
            variable=self.direction_var, 
            value="greater"
        )
        self.greater_radio.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.less_radio = ctk.CTkRadioButton(
            self.direction_frame, 
            text="Less than (<)", 
            variable=self.direction_var, 
            value="less"
        )
        self.less_radio.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Input fields
        self.create_input_field("Significance Level (α):", "sig_level", "0.05", 3)
        self.create_input_field("Probability of Success (p):", "prob_success", "0.5", 4)
        self.create_input_field("Number of Trials (n):", "num_trials", "10", 5)
        self.create_input_field("Number of Observations (x):", "num_observations", "5", 6)

        # Calculate button
        self.calculate_btn = ctk.CTkButton(
            self.main_frame, 
            text="Run Hypothesis Test", 
            command=self.run_test,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        self.calculate_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Results frame
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.results_frame.grid_columnconfigure(0, weight=1)

        self.results_label = ctk.CTkLabel(
            self.results_frame, 
            text="Results will appear here...", 
            font=ctk.CTkFont(size=14),
            wraplength=700
        )
        self.results_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Clear button
        self.clear_btn = ctk.CTkButton(
            self.main_frame, 
            text="Clear Results", 
            command=self.clear_results,
            fg_color="transparent",
            border_width=2
        )
        self.clear_btn.grid(row=9, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        # Initialize UI state
        self.on_test_type_change()

    def create_input_field(self, label_text, var_name, default_value, row):
        label = ctk.CTkLabel(self.main_frame, text=label_text, font=ctk.CTkFont(size=14))
        label.grid(row=row, column=0, padx=20, pady=(10, 5), sticky="w")
        
        entry = ctk.CTkEntry(self.main_frame, placeholder_text=default_value)
        entry.grid(row=row, column=1, padx=20, pady=(10, 5), sticky="ew")
        entry.insert(0, default_value)
        
        setattr(self, f"{var_name}_entry", entry)

    def on_test_type_change(self):
        if self.test_type_var.get() == "1-tail":
            self.direction_label.grid()
            self.direction_frame.grid()
        else:
            self.direction_label.grid_remove()
            self.direction_frame.grid_remove()

    def validate_inputs(self):
        try:
            sig_level = float(self.sig_level_entry.get())
            prob_success = float(self.prob_success_entry.get())
            num_trials = int(self.num_trials_entry.get())
            num_observations = int(self.num_observations_entry.get())
            
            # Validation checks
            if not (0 < sig_level < 1):
                raise ValueError("Significance level must be between 0 and 1")
            if not (0 <= prob_success <= 1):
                raise ValueError("Probability must be between 0 and 1")
            if num_trials <= 0:
                raise ValueError("Number of trials must be positive")
            if num_observations < 0:
                raise ValueError("Number of observations cannot be negative")
            if num_observations > num_trials:
                raise ValueError("Number of observations cannot exceed number of trials")
                
            return sig_level, prob_success, num_trials, num_observations
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None

    def run_test(self):
        inputs = self.validate_inputs()
        if inputs is None:
            return
            
        sig_level, p, n, x = inputs
        
        try:
            # Run the hypothesis test
            results = []
            results.append(f"Model: X ~ B({n}, {p})")
            
            if self.test_type_var.get() == "1-tail":
                direction = self.direction_var.get()
                
                if direction == "less":
                    results.append(f"H₀: p = {p}")
                    results.append(f"H₁: p < {p}")
                    
                    p_value = cdf(n, p, x)
                    results.append(f"P(X ≤ {x}) = {p_value:.6f}")
                    
                    if p_value < sig_level:
                        results.append(f"Since {p_value:.6f} < {sig_level}, we reject H₀")
                        results.append("Accept H₁")
                        conclusion = "There is sufficient evidence to support the alternative hypothesis."
                    else:
                        results.append(f"Since {p_value:.6f} ≥ {sig_level}, we accept H₀")
                        conclusion = "There is insufficient evidence to reject the null hypothesis."
                        
                else:  # greater
                    results.append(f"H₀: p = {p}")
                    results.append(f"H₁: p > {p}")
                    
                    p_value = 1 - cdf(n, p, x-1)
                    results.append(f"P(X ≥ {x}) = {p_value:.6f}")
                    
                    if p_value < sig_level:
                        results.append(f"Since {p_value:.6f} < {sig_level}, we reject H₀")
                        results.append("Accept H₁")
                        conclusion = "There is sufficient evidence to support the alternative hypothesis."
                    else:
                        results.append(f"Since {p_value:.6f} ≥ {sig_level}, we accept H₀")
                        conclusion = "There is insufficient evidence to reject the null hypothesis."
                        
            else:  # 2-tail
                results.append(f"H₀: p = {p}")
                results.append(f"H₁: p ≠ {p}")
                
                p_value_left = cdf(n, p, x)
                p_value_right = 1 - cdf(n, p, x-1)
                p_value = 2 * min(p_value_left, p_value_right)
                
                results.append(f"Two-tailed p-value = {p_value:.6f}")
                
                if p_value < sig_level:
                    results.append(f"Since {p_value:.6f} < {sig_level}, we reject H₀")
                    results.append("Accept H₁")
                    conclusion = "There is sufficient evidence to support the alternative hypothesis."
                else:
                    results.append(f"Since {p_value:.6f} ≥ {sig_level}, we accept H₀")
                    conclusion = "There is insufficient evidence to reject the null hypothesis."
            
            results.append(f"\nConclusion: {conclusion}")
            
            # Display results
            result_text = "\n".join(results)
            self.results_label.configure(text=result_text)
            
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred during calculation: {str(e)}")

    def clear_results(self):
        self.results_label.configure(text="Results will appear here...")
        # Reset input fields to default values
        self.sig_level_entry.delete(0, 'end')
        self.sig_level_entry.insert(0, "0.05")
        self.prob_success_entry.delete(0, 'end')
        self.prob_success_entry.insert(0, "0.5")
        self.num_trials_entry.delete(0, 'end')
        self.num_trials_entry.insert(0, "10")
        self.num_observations_entry.delete(0, 'end')
        self.num_observations_entry.insert(0, "5")

if __name__ == "__main__":
    app = StatsEngineApp()
    app.mainloop()