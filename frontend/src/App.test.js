import { render, screen, fireEvent } from '@testing-library/react';
import App from './Apppp';

test('renders the app and handles form submission', () => {
    render(<App />);
    
    const modelSelect = screen.getByLabelText(/model/i);
    const queryInput = screen.getByPlaceholderText(/enter your query/i);
    const submitButton = screen.getByText(/submit/i);
    
    // Check if elements are in the document
    expect(modelSelect).toBeInTheDocument();
    expect(queryInput).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();

    // Simulate user input
    fireEvent.change(queryInput, { target: { value: 'Hello' } });
    fireEvent.change(modelSelect, { target: { value: 'llama2' } });
    fireEvent.click(submitButton);

    // Since this is a basic test, we won't simulate the API response
    // Just check if the input value has been updated
    expect(queryInput.value).toBe('Hello');
});
