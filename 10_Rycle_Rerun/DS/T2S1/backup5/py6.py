import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import seaborn as sns

def main():
    # Configuration
    resolutions = [0.5, 1.0, 1.08, 1.5, 2.0]
    output_dir = r"C:\Users\admin\Desktop\Python_proj\ALL_RESULT\DS\T2S1\backup5"
    plots_dir = os.path.join(output_dir, "comparison_plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Load all data into a dictionary
    data = {}
    lengths = []
    for res in resolutions:
        safe_res = str(res).replace('.', '_')
        csv_path = os.path.join(output_dir, f"grayscale_values_res_{safe_res}.csv")
        if not os.path.exists(csv_path):
            print(f"Warning: CSV not found for resolution {res}")
            continue
        
        values = np.loadtxt(csv_path, delimiter=',')
        data[res] = values
        
        # Calculate pixel distance (same for all resolutions)
        if not lengths:  # Only calculate once
            start_point = (152, 29)
            end_point = (136, 91)
            x0, y0 = start_point
            x1, y1 = end_point
            pixel_distance = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        
        real_length = pixel_distance * res
        lengths.append(real_length)
    
    # Create comparative visualization
    plt.figure(figsize=(14, 14))
    gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1])
    
    # 1. Overlaid profiles plot
    ax1 = plt.subplot(gs[0, :])
    for res, values in data.items():
        ax1.plot(values, label=f'{res} units/pixel', alpha=0.8)
    ax1.set_title('Comparative Grayscale Profiles')
    ax1.set_xlabel('Pixel Position Along Line')
    ax1.set_ylabel('Grayscale Value (0-255)')
    ax1.legend()
    ax1.grid(alpha=0.2)
    
    # 2. Statistical comparison
    ax2 = plt.subplot(gs[1, 0])
    stats = []
    for res, values in data.items():
        stats.append({
            'Resolution': res,
            'Mean': np.mean(values),
            'Median': np.median(values),
            'Min': np.min(values),
            'Max': np.max(values),
            'Std Dev': np.std(values)
        })
    df = pd.DataFrame(stats)
    df.set_index('Resolution', inplace=True)
    
    sns.heatmap(df, annot=True, fmt='.2f', cmap='viridis', ax=ax2)
    ax2.set_title('Statistical Comparison')
    
    # 3. Length vs. Resolution
    ax3 = plt.subplot(gs[1, 1])
    ax3.plot(resolutions, lengths, 'o-', color='darkred')
    ax3.set_title('Real Length vs. Resolution')
    ax3.set_xlabel('Resolution (units/pixel)')
    ax3.set_ylabel('Real Length (units)')
    ax3.grid(alpha=0.2)
    
    # 4. Min/Max comparison
    ax4 = plt.subplot(gs[2, 0])
    min_vals = [np.min(v) for v in data.values()]
    max_vals = [np.max(v) for v in data.values()]
    
    x = np.arange(len(resolutions))
    width = 0.35
    ax4.bar(x - width/2, min_vals, width, label='Min Value', color='navy')
    ax4.bar(x + width/2, max_vals, width, label='Max Value', color='crimson')
    ax4.set_title('Min/Max Grayscale Values')
    ax4.set_xticks(x)
    ax4.set_xticklabels(resolutions)
    ax4.set_xlabel('Resolution')
    ax4.legend()
    
    # 5. Profile variability
    ax5 = plt.subplot(gs[2, 1])
    std_devs = [np.std(v) for v in data.values()]
    ax5.plot(resolutions, std_devs, 's-', color='darkgreen')
    ax5.set_title('Profile Variability (Standard Deviation)')
    ax5.set_xlabel('Resolution')
    ax5.set_ylabel('Standard Deviation')
    ax5.grid(alpha=0.2)
    
    # Finalize layout
    plt.tight_layout()
    comparison_path = os.path.join(plots_dir, "comprehensive_comparison.png")
    plt.savefig(comparison_path, dpi=150)
    plt.close()
    print(f"Comprehensive comparison saved: {comparison_path}")
    
    # Create individual profile plots
    print("\nCreating individual profile plots:")
    for res, values in data.items():
        plt.figure(figsize=(10, 6))
        plt.plot(values, 'b-', linewidth=1.5)
        plt.title(f"Grayscale Profile (Resolution: {res})")
        plt.xlabel("Pixel Position")
        plt.ylabel("Grayscale Value")
        plt.grid(alpha=0.2)
        
        plot_path = os.path.join(plots_dir, f"individual_profile_res_{res}.png")
        plt.savefig(plot_path, dpi=120)
        plt.close()
        print(f"- Created: {plot_path}")
    
    # Generate CSV comparison
    comparison_csv = os.path.join(output_dir, "profile_statistics.csv")
    df.to_csv(comparison_csv)
    print(f"\nStatistics CSV saved: {comparison_csv}")
    
    print("\nComparative analysis complete!")

if __name__ == "__main__":
    main()
