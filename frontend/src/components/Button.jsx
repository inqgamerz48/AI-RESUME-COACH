/**
 * Reusable Button Component
 */
export default function Button({
    children,
    variant = 'primary',
    onClick,
    disabled = false,
    className = '',
    type = 'button'
}) {
    const variantClasses = {
        primary: 'btn-primary',
        secondary: 'btn-secondary',
        upgrade: 'btn-upgrade',
    };

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${variantClasses[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
        >
            {children}
        </button>
    );
}
