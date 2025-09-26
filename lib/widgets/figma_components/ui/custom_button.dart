import 'package:flutter/material.dart';
import '../../../theme/app_theme.dart';

enum ButtonVariant {
  primary,
  secondary,
  outline,
  ghost,
  destructive,
}

enum ButtonSize {
  sm,
  default_,
  lg,
  icon,
}

class CustomButton extends StatelessWidget {
  final String? text;
  final IconData? icon;
  final VoidCallback? onPressed;
  final ButtonVariant variant;
  final ButtonSize size;
  final bool isLoading;
  final bool isDisabled;

  const CustomButton({
    super.key,
    this.text,
    this.icon,
    this.onPressed,
    this.variant = ButtonVariant.primary,
    this.size = ButtonSize.default_,
    this.isLoading = false,
    this.isDisabled = false,
  });

  @override
  Widget build(BuildContext context) {
    final isEnabled = onPressed != null && !isDisabled && !isLoading;
    
    return _buildButton(context, isEnabled);
  }

  Widget _buildButton(BuildContext context, bool isEnabled) {
    switch (variant) {
      case ButtonVariant.primary:
        return _buildElevatedButton(context, isEnabled);
      case ButtonVariant.secondary:
        return _buildSecondaryButton(context, isEnabled);
      case ButtonVariant.outline:
        return _buildOutlinedButton(context, isEnabled);
      case ButtonVariant.ghost:
        return _buildTextButton(context, isEnabled);
      case ButtonVariant.destructive:
        return _buildDestructiveButton(context, isEnabled);
    }
  }

  Widget _buildElevatedButton(BuildContext context, bool isEnabled) {
    return ElevatedButton(
      onPressed: isEnabled ? onPressed : null,
      style: ElevatedButton.styleFrom(
        backgroundColor: isEnabled ? AppTheme.primaryBlue : AppTheme.textTertiary,
        foregroundColor: Colors.white,
        elevation: 0,
        padding: _getPadding(),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(_getBorderRadius()),
        ),
        textStyle: _getTextStyle(),
      ),
      child: _buildChild(),
    );
  }

  Widget _buildSecondaryButton(BuildContext context, bool isEnabled) {
    return ElevatedButton(
      onPressed: isEnabled ? onPressed : null,
      style: ElevatedButton.styleFrom(
        backgroundColor: isEnabled ? AppTheme.surfaceBlue : AppTheme.textTertiary,
        foregroundColor: isEnabled ? AppTheme.primaryBlue : Colors.white,
        elevation: 0,
        padding: _getPadding(),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(_getBorderRadius()),
        ),
        textStyle: _getTextStyle(),
      ),
      child: _buildChild(),
    );
  }

  Widget _buildOutlinedButton(BuildContext context, bool isEnabled) {
    return OutlinedButton(
      onPressed: isEnabled ? onPressed : null,
      style: OutlinedButton.styleFrom(
        foregroundColor: isEnabled ? AppTheme.primaryBlue : AppTheme.textTertiary,
        side: BorderSide(
          color: isEnabled ? AppTheme.primaryBlue : AppTheme.textTertiary,
          width: 1.5,
        ),
        padding: _getPadding(),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(_getBorderRadius()),
        ),
        textStyle: _getTextStyle(),
      ),
      child: _buildChild(),
    );
  }

  Widget _buildTextButton(BuildContext context, bool isEnabled) {
    return TextButton(
      onPressed: isEnabled ? onPressed : null,
      style: TextButton.styleFrom(
        foregroundColor: isEnabled ? AppTheme.primaryBlue : AppTheme.textTertiary,
        padding: _getPadding(),
        textStyle: _getTextStyle(),
      ),
      child: _buildChild(),
    );
  }

  Widget _buildDestructiveButton(BuildContext context, bool isEnabled) {
    return ElevatedButton(
      onPressed: isEnabled ? onPressed : null,
      style: ElevatedButton.styleFrom(
        backgroundColor: isEnabled ? const Color(0xFFDC2626) : AppTheme.textTertiary,
        foregroundColor: Colors.white,
        elevation: 0,
        padding: _getPadding(),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(_getBorderRadius()),
        ),
        textStyle: _getTextStyle(),
      ),
      child: _buildChild(),
    );
  }

  Widget _buildChild() {
    if (isLoading) {
      return SizedBox(
        width: _getIconSize(),
        height: _getIconSize(),
        child: const CircularProgressIndicator(
          strokeWidth: 2,
          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
        ),
      );
    }

    if (icon != null && text != null) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: _getIconSize()),
          const SizedBox(width: 8),
          Text(text!),
        ],
      );
    } else if (icon != null) {
      return Icon(icon, size: _getIconSize());
    } else {
      return Text(text ?? '');
    }
  }

  EdgeInsets _getPadding() {
    switch (size) {
      case ButtonSize.sm:
        return const EdgeInsets.symmetric(horizontal: 12, vertical: 8);
      case ButtonSize.default_:
        return const EdgeInsets.symmetric(horizontal: 16, vertical: 12);
      case ButtonSize.lg:
        return const EdgeInsets.symmetric(horizontal: 20, vertical: 16);
      case ButtonSize.icon:
        return const EdgeInsets.all(12);
    }
  }

  double _getBorderRadius() {
    switch (size) {
      case ButtonSize.sm:
        return 8;
      case ButtonSize.default_:
        return 12;
      case ButtonSize.lg:
        return 16;
      case ButtonSize.icon:
        return 8;
    }
  }

  TextStyle _getTextStyle() {
    switch (size) {
      case ButtonSize.sm:
        return AppTheme.koreanTextStyle(fontSize: 14, fontWeight: FontWeight.w500);
      case ButtonSize.default_:
        return AppTheme.koreanTextStyle(fontSize: 16, fontWeight: FontWeight.w600);
      case ButtonSize.lg:
        return AppTheme.koreanTextStyle(fontSize: 18, fontWeight: FontWeight.w600);
      case ButtonSize.icon:
        return AppTheme.koreanTextStyle(fontSize: 16, fontWeight: FontWeight.w500);
    }
  }

  double _getIconSize() {
    switch (size) {
      case ButtonSize.sm:
        return 16;
      case ButtonSize.default_:
        return 20;
      case ButtonSize.lg:
        return 24;
      case ButtonSize.icon:
        return 20;
    }
  }
}
