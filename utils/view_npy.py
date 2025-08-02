#!/usr/bin/env python3
"""
Utility script to view the contents of generated database .npy files.
To obtain .npy files, first unzip the database .npz file, and then run this script on each .npy file.
Made with ❤️ by ChatGPT.
"""

import numpy as np
import argparse
import sys
from pathlib import Path


def view_npy_file(filepath, max_elements=10, show_stats=True, show_sample=True):
    """
    View the contents of a NumPy .npy file.
    
    Args:
        filepath (str): Path to the .npy file
        max_elements (int): Maximum number of elements to display
        show_stats (bool): Whether to show statistical information
        show_sample (bool): Whether to show sample data
    """
    try:
        # Load the numpy array
        data = np.load(filepath)
        
        print(f"File: {filepath}")
        print("=" * 50)
        
        # Basic information
        print(f"Data type: {data.dtype}")
        print(f"Shape: {data.shape}")
        print(f"Number of dimensions: {data.ndim}")
        print(f"Total elements: {data.size}")
        print(f"Memory usage: {data.nbytes} bytes ({data.nbytes / 1024:.2f} KB, {data.nbytes / (1024*1024):.2f} MB)")
        
        # Statistical information for numeric data
        if show_stats and np.issubdtype(data.dtype, np.number):
            print("\nStatistical Information:")
            print("-" * 30)
            print(f"Min value: {np.min(data)}")
            print(f"Max value: {np.max(data)}")
            print(f"Mean: {np.mean(data):.6f}")
            print(f"Standard deviation: {np.std(data):.6f}")
            
            # Show unique values if array is small or has few unique values
            if data.size <= 1000:
                unique_vals = np.unique(data)
                if len(unique_vals) <= 20:
                    print(f"Unique values ({len(unique_vals)}): {unique_vals}")
        
        # Sample data
        if show_sample:
            print(f"\nSample Data (showing up to {max_elements} elements):")
            print("-" * 30)
            
            if data.size == 0:
                print("Array is empty")
            elif data.ndim == 1:
                # 1D array
                sample_size = min(max_elements, data.size)
                print(f"First {sample_size} elements:")
                print(data[:sample_size])
                if data.size > max_elements:
                    print("...")
                    print(f"Last {min(5, data.size - max_elements)} elements:")
                    print(data[-min(5, data.size - max_elements):])
            elif data.ndim == 2:
                # 2D array
                rows_to_show = min(max_elements, data.shape[0])
                cols_to_show = min(10, data.shape[1])
                print(f"First {rows_to_show} rows, {cols_to_show} columns:")
                print(data[:rows_to_show, :cols_to_show])
                if data.shape[0] > max_elements or data.shape[1] > 10:
                    print("...")
            else:
                # Higher dimensional arrays
                print("Shape:", data.shape)
                flat_data = data.flatten()
                sample_size = min(max_elements, flat_data.size)
                print(f"First {sample_size} elements (flattened):")
                print(flat_data[:sample_size])
                if flat_data.size > max_elements:
                    print("...")
        
        # Additional information for structured arrays
        if data.dtype.names is not None:
            print(f"\nStructured Array Field Names:")
            print("-" * 30)
            for name in data.dtype.names:
                field_dtype = data.dtype.fields[name][0]
                print(f"  {name}: {field_dtype}")
    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return False
    except Exception as e:
        print(f"Error loading file: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="View contents of NumPy .npy files")
    parser.add_argument("filepath", help="Path to the .npy file")
    parser.add_argument("--max-elements", "-n", type=int, default=10,
                       help="Maximum number of elements to display (default: 10)")
    parser.add_argument("--no-stats", action="store_true",
                       help="Don't show statistical information")
    parser.add_argument("--no-sample", action="store_true", 
                       help="Don't show sample data")
    
    args = parser.parse_args()
    
    # Check if file exists
    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File '{filepath}' does not exist.")
        sys.exit(1)
    
    if not filepath.suffix.lower() == '.npy':
        print(f"Warning: File '{filepath}' does not have .npy extension.")
    
    success = view_npy_file(
        filepath,
        max_elements=args.max_elements,
        show_stats=not args.no_stats,
        show_sample=not args.no_sample
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
