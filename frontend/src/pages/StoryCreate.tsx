import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { createStory } from '../services/stories';
import { STORY_CATEGORIES, STORY_CATEGORY_LABELS } from '../constants/story';
import LocationPickerMap from '../components/map/LocationPickerMap';
import type { StoryCreateRequest, StoryCategory } from '../types';

interface FormData {
  title: string;
  body: string;
  category: StoryCategory | '';
  location_lat: string;
  location_lng: string;
  date_of_story: string;
}

interface ValidationErrors {
  title?: string;
  location_lat?: string;
  location_lng?: string;
  date_of_story?: string;
}

function StoryCreate() {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<FormData>({
    title: '',
    body: '',
    category: '',
    location_lat: '',
    location_lng: '',
    date_of_story: '',
  });
  
  const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const validateForm = (): boolean => {
    const errors: ValidationErrors = {};
    
    // Title validation
    if (!formData.title.trim()) {
      errors.title = 'Title is required';
    }
    
    // Latitude validation
    if (!formData.location_lat) {
      errors.location_lat = 'Latitude is required';
    } else {
      const lat = parseFloat(formData.location_lat);
      if (isNaN(lat) || lat < -90 || lat > 90) {
        errors.location_lat = 'Latitude must be between -90 and 90';
      }
    }
    
    // Longitude validation
    if (!formData.location_lng) {
      errors.location_lng = 'Longitude is required';
    } else {
      const lng = parseFloat(formData.location_lng);
      if (isNaN(lng) || lng < -180 || lng > 180) {
        errors.location_lng = 'Longitude must be between -180 and 180';
      }
    }
    
    // Date validation (must not be in the future)
    if (formData.date_of_story) {
      const storyDate = new Date(formData.date_of_story);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (storyDate > today) {
        errors.date_of_story = 'Story date cannot be in the future';
      }
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);

    try {
      const payload: StoryCreateRequest = {
        title: formData.title.trim(),
        body: formData.body.trim() || null,
        category: formData.category || null,
        location_lat: parseFloat(formData.location_lat),
        location_lng: parseFloat(formData.location_lng),
        date_of_story: formData.date_of_story || null,
      };
      
      await createStory(payload);
      setSuccess(true);
      
      // Navigate after a brief success message
      setTimeout(() => {
        navigate('/');
      }, 1000);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create story. Please try again.';
      setError(errorMessage);
      console.error('Error creating story:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    navigate('/');
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // Clear validation error for this field when user starts typing
    if (validationErrors[field as keyof ValidationErrors]) {
      setValidationErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[field as keyof ValidationErrors];
        return newErrors;
      });
    }
  };

  const handleMapLocationSelect = (coords: { lat: number; lng: number }) => {
    setFormData((prev) => ({
      ...prev,
      location_lat: coords.lat.toFixed(6),
      location_lng: coords.lng.toFixed(6),
    }));
    // Clear location validation errors
    setValidationErrors((prev) => {
      const newErrors = { ...prev };
      delete newErrors.location_lat;
      delete newErrors.location_lng;
      return newErrors;
    });
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: 'var(--spacing-lg)' }}>Create New Story</h1>

      {error && (
        <calcite-notice kind="danger" open closable style={{ marginBottom: 'var(--spacing-lg)' }}>
          <div slot="title">Error</div>
          <div slot="message">{error}</div>
        </calcite-notice>
      )}

      {success && (
        <calcite-notice kind="success" open style={{ marginBottom: 'var(--spacing-lg)' }}>
          <div slot="title">Success</div>
          <div slot="message">Story created successfully! Redirecting...</div>
        </calcite-notice>
      )}

      <calcite-panel>
        <form onSubmit={handleSubmit} style={{ padding: 'var(--spacing-lg)' }}>
          {/* Title */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <calcite-label scale="m" layout="default">
              Title
              <span style={{ color: 'var(--color-error)' }}> *</span>
              <calcite-input
                type="text"
                value={formData.title}
                onCalciteInputInput={(e: any) => handleInputChange('title', e.target.value)}
                placeholder="Enter story title"
                scale="m"
                status={validationErrors.title ? 'invalid' : 'idle'}
                maxLength={500}
                required
              />
              {validationErrors.title && (
                <calcite-input-message status="invalid" scale="m">
                  {validationErrors.title}
                </calcite-input-message>
              )}
            </calcite-label>
          </div>

          {/* Body */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <calcite-label scale="m" layout="default">
              Story Content
              <calcite-text-area
                value={formData.body}
                onCalciteTextAreaInput={(e: any) => handleInputChange('body', e.target.value)}
                placeholder="Tell your story... (supports markdown, max 50,000 characters)"
                scale="m"
                rows={8}
                maxLength={50000}
                resize="vertical"
              />
              <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginTop: 'var(--spacing-xs)' }}>
                {formData.body.length} / 50,000 characters
              </div>
            </calcite-label>
          </div>

          {/* Category */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <calcite-label scale="m" layout="default">
              Category
              <calcite-select
                value={formData.category}
                onCalciteSelectChange={(e: any) => handleInputChange('category', e.target.value)}
                scale="m"
                width="full"
              >
                <calcite-option value="" label="Select a category (optional)"></calcite-option>
                {STORY_CATEGORIES.map((cat) => (
                  <calcite-option key={cat} value={cat} label={STORY_CATEGORY_LABELS[cat]}></calcite-option>
                ))}
              </calcite-select>
            </calcite-label>
          </div>

          {/* Date */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <calcite-label scale="m" layout="default">
              Date of Story
              <calcite-input
                type="date"
                value={formData.date_of_story}
                onCalciteInputInput={(e: any) => handleInputChange('date_of_story', e.target.value)}
                scale="m"
                status={validationErrors.date_of_story ? 'invalid' : 'idle'}
                max={new Date().toISOString().split('T')[0]}
              />
              {validationErrors.date_of_story && (
                <calcite-input-message status="invalid" scale="m">
                  {validationErrors.date_of_story}
                </calcite-input-message>
              )}
            </calcite-label>
          </div>

          {/* Location */}
          <div style={{ marginBottom: 'var(--spacing-lg)' }}>
            <h3 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--spacing-md)' }}>
              Location <span style={{ color: 'var(--color-error)' }}>*</span>
            </h3>
            
            {/* Map Location Picker */}
            <div style={{ marginBottom: 'var(--spacing-md)' }}>
              <div style={{ 
                fontSize: 'var(--font-size-sm)', 
                color: 'var(--color-text-secondary)',
                marginBottom: 'var(--spacing-xs)'
              }}>
                Click the map to set coordinates
              </div>
              <LocationPickerMap
                value={
                  formData.location_lat && formData.location_lng
                    ? {
                        lat: parseFloat(formData.location_lat),
                        lng: parseFloat(formData.location_lng),
                      }
                    : null
                }
                onChange={handleMapLocationSelect}
                height={320}
              />
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--spacing-md)' }}>
              {/* Latitude */}
              <calcite-label scale="m" layout="default">
                Latitude
                <calcite-input
                  type="number"
                  value={formData.location_lat}
                  onCalciteInputInput={(e: any) => handleInputChange('location_lat', e.target.value)}
                  placeholder="-90 to 90"
                  scale="m"
                  status={validationErrors.location_lat ? 'invalid' : 'idle'}
                  step="any"
                  min={-90}
                  max={90}
                  required
                />
                {validationErrors.location_lat && (
                  <calcite-input-message status="invalid" scale="m">
                    {validationErrors.location_lat}
                  </calcite-input-message>
                )}
              </calcite-label>

              {/* Longitude */}
              <calcite-label scale="m" layout="default">
                Longitude
                <calcite-input
                  type="number"
                  value={formData.location_lng}
                  onCalciteInputInput={(e: any) => handleInputChange('location_lng', e.target.value)}
                  placeholder="-180 to 180"
                  scale="m"
                  status={validationErrors.location_lng ? 'invalid' : 'idle'}
                  step="any"
                  min={-180}
                  max={180}
                  required
                />
                {validationErrors.location_lng && (
                  <calcite-input-message status="invalid" scale="m">
                    {validationErrors.location_lng}
                  </calcite-input-message>
                )}
              </calcite-label>
            </div>
            
            <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginTop: 'var(--spacing-sm)' }}>
              Enter coordinates manually or use the map picker (coming soon)
            </div>
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: 'var(--spacing-md)', marginTop: 'var(--spacing-xl)' }}>
            <calcite-button
              type="submit"
              appearance="solid"
              kind="brand"
              scale="m"
              width="auto"
              loading={isSubmitting}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Creating...' : 'Create Story'}
            </calcite-button>
            
            <calcite-button
              type="button"
              appearance="outline"
              kind="neutral"
              scale="m"
              width="auto"
              onClick={handleCancel}
              disabled={isSubmitting}
            >
              Cancel
            </calcite-button>
          </div>
        </form>
      </calcite-panel>
    </div>
  );
}

export default StoryCreate;
