import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApiService } from '../../services/api';

interface PricingTier {
  name: string;
  price: number;
  yearlyPrice: number;
  description: string;
  features: string[];
  notIncluded?: string[];
  highlighted: boolean;
  cta: string;
  priceId?: string;
}

@Component({
  selector: 'app-pricing',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './pricing.html',
  styleUrl: './pricing.css',
})
export class Pricing {
  isYearly: boolean = true;
  isLoggedIn: boolean = false;

  tiers: PricingTier[] = [
    {
      name: 'Free',
      price: 0,
      yearlyPrice: 0,
      description: 'Perfect for getting started with portfolio tracking',
      features: [
        'Up to 10 holdings',
        '1 price alert',
        '5 stock lookups per day',
        'Basic portfolio dashboard',
        'Transaction history',
        'Manual CSV import'
      ],
      notIncluded: [
        'AI insights & recommendations',
        'Price predictions',
        'Unlimited alerts',
        'Realized/unrealized gains',
        'Weekly digest reports',
        'Priority support'
      ],
      highlighted: false,
      cta: 'Get Started'
    },
    {
      name: 'Pro',
      price: 9.99,
      yearlyPrice: 79,
      description: 'For serious investors who want deeper insights',
      features: [
        'Unlimited holdings',
        'Unlimited price alerts',
        'Unlimited stock lookups',
        'AI-powered insights',
        '30-day price predictions',
        'Realized & unrealized gains',
        'Weekly portfolio digest',
        'CSV import & export',
        'Email notifications',
        'Priority support'
      ],
      highlighted: true,
      cta: 'Start Pro Trial',
      priceId: 'price_pro_monthly'
    },
    {
      name: 'Pro+',
      price: 19.99,
      yearlyPrice: 149,
      description: 'Maximum power for professional traders',
      features: [
        'Everything in Pro',
        '90-day price predictions',
        'Multiple portfolios',
        'API access',
        'Tax-loss harvesting tips',
        'Portfolio optimization',
        'Advanced analytics',
        'Dividend tracking & forecasts',
        'White-glove onboarding',
        'Dedicated support'
      ],
      highlighted: false,
      cta: 'Start Pro+ Trial',
      priceId: 'price_proplus_monthly'
    }
  ];

  faqs = [
    {
      question: 'Can I cancel anytime?',
      answer: 'Yes, you can cancel your subscription at any time. You\'ll continue to have access until the end of your billing period.'
    },
    {
      question: 'Is there a free trial?',
      answer: 'Yes! Pro and Pro+ plans come with a 14-day free trial. No credit card required to start.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards (Visa, Mastercard, American Express) and debit cards through our secure payment processor, Stripe.'
    },
    {
      question: 'Can I switch plans?',
      answer: 'Absolutely! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate your billing.'
    },
    {
      question: 'Is my financial data secure?',
      answer: 'This is currently a demo project. In a production version, we would implement bank-level encryption (AES-256) and never store your brokerage credentials. Your data is yours and we never sell it.-'
    },
    {
      question: 'Do you offer refunds?',
      answer: 'Yes, we offer a 30-day money-back guarantee. If you\'re not satisfied, contact us for a full refund.'
    }
  ];

  isLoading: boolean = false;

  constructor(
    private authService: AuthService,
    private apiService: ApiService
  ) {
    this.isLoggedIn = this.authService.isLoggedIn();
  }

  toggleBilling(): void {
    this.isYearly = !this.isYearly;
  }

  getPrice(tier: PricingTier): number {
    if (tier.price === 0) return 0;
    return this.isYearly ? tier.yearlyPrice : tier.price;
  }

  getPriceLabel(tier: PricingTier): string {
    if (tier.price === 0) return 'Free forever';
    return this.isYearly ? '/year' : '/month';
  }

  getSavings(tier: PricingTier): number {
    if (tier.price === 0) return 0;
    const monthlyTotal = tier.price * 12;
    return Math.round(((monthlyTotal - tier.yearlyPrice) / monthlyTotal) * 100);
  }

  selectPlan(tier: PricingTier): void {
    if (tier.price === 0) {
      // Free tier - redirect to register or dashboard
      if (this.isLoggedIn) {
        window.location.href = '/dashboard';
      } else {
        window.location.href = '/register';
      }
    } else {
      // Paid tier - create checkout session
      if (!this.isLoggedIn) {
        window.location.href = '/register?plan=' + tier.name.toLowerCase();
      } else {
        this.isLoading = true;
        const planName = tier.name === 'Pro+' ? 'pro_plus' : 'pro';

        this.apiService.createCheckout(planName).subscribe({
          next: (response) => {
            // Redirect to Stripe checkout
            window.location.href = response.checkout_url;
          },
          error: (err) => {
            this.isLoading = false;
            console.error('Checkout error:', err);
            alert('Unable to start checkout. Please try again or contact support.');
          }
        });
      }
    }
  }
}
