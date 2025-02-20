def calculate_statistics(data):
    statistics = {
        'Sales': {
            'total': f"{data['Sales'].sum():.5f}",
            'mean': f"{data['Sales'].mean():.5f}",
            'median': f"{data['Sales'].median():.5f}",
            'mode': f"{data['Sales'].mode()[0]:.5f}",  # Mode returns a Series, take first value
            'std': f"{data['Sales'].std():.5f}"
        },
        'Profit': {
            'total': f"{data['Profit'].sum():.5f}",
            'mean': f"{data['Profit'].mean():.5f}",
            'median': f"{data['Profit'].median():.5f}",
            'mode': f"{data['Profit'].mode()[0]:.5f}",
            'std': f"{data['Profit'].std():.5f}"
        },
        'Quantity': {
            'total': f"{data['Quantity'].sum():.5f}",
            'mean': f"{data['Quantity'].mean():.5f}",
            'median': f"{data['Quantity'].median():.5f}",
            'mode': f"{data['Quantity'].mode()[0]:.5f}",
            'std': f"{data['Quantity'].std():.5f}"
        },
        'Region': {
            'max_sales': {
                'region': data.groupby('Region')['Sales'].sum().idxmax(),
                'value': f"{data.groupby('Region')['Sales'].sum().max():.3f}",
                'advice': " Give Good Customer Service to Maintain Sales."
            },
            'min_sales': {
                'region': data.groupby('Region')['Sales'].sum().idxmin(),
                'value': f"{data.groupby('Region')['Sales'].sum().min():.3f}",
                'advice': "  Consider marketing strategies to boost sales."
            },
            'max_profit': {
                'region': data.groupby('Region')['Profit'].sum().idxmax(),
                'value': f"{data.groupby('Region')['Profit'].sum().max():.3f}",
                'advice': " Expand product range in this region to Increse Profit."
            },
            'min_profit': {
                'region': data.groupby('Region')['Profit'].sum().idxmin(),
                'value': f"{data.groupby('Region')['Profit'].sum().min():.3f}",
                'advice': " Increase profit margin strategies in this region."
            }
        },
        'Category': {
            'max_sales': {
                'category': data.groupby('Category')['Sales'].sum().idxmax(),
                'value': f"{data.groupby('Category')['Sales'].sum().max():.3f}",
                'advice': " Maintain strong supply chain in this category."
            },
            'min_sales': {
                'category': data.groupby('Category')['Sales'].sum().idxmin(),
                'value': f"{data.groupby('Category')['Sales'].sum().min():.3f}",
                'advice': "  Consider removing low-selling items from inventory."
            },
            'max_profit': {
                'category': data.groupby('Category')['Profit'].sum().idxmax(),
                'value': f"{data.groupby('Category')['Profit'].sum().max():.3f}",
                'advice': " Increase investment in high-margin products."
            },
            'min_profit': {
                'category': data.groupby('Category')['Profit'].sum().idxmin(),
                'value': f"{data.groupby('Category')['Profit'].sum().min():.3f}",
                'advice': "  Consider adjusting pricing or cost structure."
            }
        },
        'SubCategory': {
            'min_sales': {
                'subcategory': data.groupby('SubCategory')['Sales'].sum().idxmin(),
                'value': f"{data.groupby('SubCategory')['Sales'].sum().min():.3f}",
                'advice': "Evaluate discontinuation of low-selling subcategory."
            }
        }
    }
    
    return statistics