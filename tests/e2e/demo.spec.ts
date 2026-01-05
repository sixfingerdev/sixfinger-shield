import { test, expect } from '@playwright/test';

test.describe('SixFinger Shield Demo', () => {
  test('should display the main page', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('h1')).toContainText('SixFinger Shield');
    await expect(page.locator('text=Generate Fingerprint')).toBeVisible();
  });

  test('should generate a fingerprint', async ({ page }) => {
    await page.goto('/');
    
    // Click generate button
    await page.click('text=Generate Fingerprint');
    
    // Wait for fingerprint to be generated
    await expect(page.locator('text=Fingerprint Hash')).toBeVisible({ timeout: 10000 });
    
    // Check if hash is displayed (32 characters)
    const hashElement = page.locator('.font-mono.text-2xl').first();
    await expect(hashElement).toBeVisible();
    
    const hashText = await hashElement.textContent();
    expect(hashText).toBeTruthy();
    expect(hashText?.length).toBe(32);
  });

  test('should display risk assessment', async ({ page }) => {
    await page.goto('/');
    
    // Click generate button
    await page.click('text=Generate Fingerprint');
    
    // Wait for risk assessment
    await expect(page.locator('text=Risk Assessment')).toBeVisible({ timeout: 10000 });
    
    // Check if score is displayed
    await expect(page.locator('text=Score')).toBeVisible();
    await expect(page.locator('text=Status')).toBeVisible();
    await expect(page.locator('text=Visits')).toBeVisible();
  });

  test('should display browser signals', async ({ page }) => {
    await page.goto('/');
    
    // Click generate button
    await page.click('text=Generate Fingerprint');
    
    // Wait for components
    await expect(page.locator('text=Browser Signals')).toBeVisible({ timeout: 10000 });
    
    // Check if at least 15 components are displayed
    const components = page.locator('.border.border-gray-200.dark\\:border-gray-700.rounded.p-3');
    await expect(components.first()).toBeVisible();
    
    const count = await components.count();
    expect(count).toBeGreaterThanOrEqual(15);
  });

  test('should display features section', async ({ page }) => {
    await page.goto('/');
    
    await expect(page.locator('text=Features')).toBeVisible();
    await expect(page.locator('text=15+ Browser Signals')).toBeVisible();
    await expect(page.locator('text=32-char Unique Hash')).toBeVisible();
    await expect(page.locator('text=Bot Detection')).toBeVisible();
    await expect(page.locator('text=Client-side Only')).toBeVisible();
  });
});
