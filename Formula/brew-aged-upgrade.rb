# typed: false
# frozen_string_literal: true

class BrewAgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after they have been outdated for N days"
  homepage "https://github.com/nhm7/brew-aged-upgrade"
  url "https://github.com/nhm7/brew-aged-upgrade/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "744c9a11f264de6a5634db080ac5872bfc7129e5c563adf221ea27dfab36ca40"
  version "1.0.0"

  head "https://github.com/nhm7/brew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on :macos
  uses_from_macos "python3"

  def install
    libexec.install "libexec/brew-aged-upgrade", "libexec/brew-aged-upgrade-core.py"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  test do
    output = shell_output("#{bin}/brew-aged-upgrade help")
    assert_match "start", output
    assert_match "stop", output
    assert_match "status", output
  end
end
